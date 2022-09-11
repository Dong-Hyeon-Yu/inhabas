from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from DB.models import User, UserAuth, UserRole, QuestForm, Answer, MajorInfo, PolicyTerms, UserSchedule, \
    UserSocialAccount, AuthUser
from django.http import HttpResponseRedirect, JsonResponse
from . import session
from urllib.request import urlretrieve  # 인터넷에 있는 파일 다운로드
import os
from django.conf import settings
from user_controller import get_social_login_info
from django.db import transaction
from date_controller import user_recruit_check, is_user_recruiting
from django.contrib import messages
from alarm.alarm_controller import create_user_join_alarm
from user_controller import get_default_pic_path


# util
def check_required_consent_fields(social_dict):
    if social_dict["email"] is None:
        raise AttributeError('no email')


# @PendingDeprecationWarning
def user_has_already_joined(request, social_dict) -> bool:
    """
        기존에는 OAuth2 인증 후, 해당 이메일과 회원 학번을 연결하여 회원가입된 유저인지 확인했었다.
        하지만 naver oauth2 의 경우 사용자 연락처 이메일을 변경할 수 있음이 발견되어,
        (provider, uid) 로 소셜계정을 구분하도록 변경했다.
        이미 회원이지만 이 변경사항 적용 후에 아직 uid 가 매핑되지 않은 회원이 존재할 수 있다.
        따라서 호환성을 위해 email 로 소셜 계정을 한번 더 찾고, 있을 경우 uid 를 추가하도록 했다.

        https://github.com/InhaBas/Inhabas.com/issues/102
    """
    if user_social_account := UserSocialAccount.objects.select_related("user") \
            .filter(email=social_dict.get("email"), provider=social_dict.get("provider")).first():
        user_social_account.uid = social_dict.get("uid")
        user_social_account.save()

        session.save_session(request,
                             user_model=user_social_account.user,
                             logined_email=user_social_account.email,
                             provider=user_social_account.provider)
        return True

    return False


def choose_std_or_pro(request):  # 학생인지, 교수인지 고르는 페이지. (회원가입 시작지점)

    if request.method != "POST":
        messages.warning(request, "비정상적인 접근입니다!")

    elif request.POST.get("password") is None:
        messages.warning(request, "소셜 로그인에 실패했습니다. 다시 시도해주세요!")

    else:
        user_token = request.POST.get("password")  # 토큰 정보를 받음

        social_dict = None
        try:
            social_dict = get_social_login_info(user_token)

            user_social_account = UserSocialAccount.objects.select_related("user") \
                .get(uid=social_dict.get("uid"), provider=social_dict.get("provider"))

            session.save_session(request,
                                 user_model=user_social_account.user,
                                 logined_email=user_social_account.email,
                                 provider=user_social_account.provider)

        except UserSocialAccount.DoesNotExist:

            if not user_has_already_joined(request, social_dict):

                if is_user_recruiting():
                    return render(request, 'std_or_pro.html', social_dict)
                else:
                    messages.warning(request, "입부 신청 기간이 아닙니다.")

        except AuthUser.DoesNotExist or SocialAccount.DoesNotExist:
            messages.warning(request, "소셜 로그인에 실패했습니다. 다시 시도해주세요!")

        except AttributeError:
            messages.warning(request, "소셜로그인 필수 동의 항목 값을 불러올 수 없습니다. 소셜 계정에서 관련 설정을 변경해주세요!")

    return redirect("index")


@user_recruit_check
def join(request):  # 회원 가입 페이지를 랜더링 하는 함수
    if request.method == "POST":

        context = {  # hidden을 통해서 받은 회원들의 정보를 받아서 붙여넣음.
            "email": request.POST.get("email"),
            "name": request.POST.get("name"),
            "pic": request.POST.get("pic"),
            "provider": request.POST.get("provider"),
            "uid": request.POST.get("uid"),
            "user_role": request.POST.get("user_role"),  # 회원 역할 (학생 or 교수)
            "quest_list": QuestForm.objects.all(),  # 질문 양식
            "major_list": MajorInfo.objects.all()  # 전공 리스트(전공 검색을 위해)
        }
        return render(request, "join.html", context)

    # 회원가입 폼 제출 전에, 사용자가 입력한 학번과 핸드폰 번호를 db와 비교 후 중복여부 알려줌
    if request.method == "GET":
        user_stu = request.GET.get('user_stu', '')
        user_phone = request.GET.get('user_phone', '')

        if user_stu:
            if len(User.objects.filter(user_stu=user_stu)):
                return JsonResponse(status=400, data={})
            else:
                return JsonResponse(status=200, data={})

        elif user_phone:
            if len(User.objects.filter(user_phone=user_phone)):
                return JsonResponse(status=400, data={})
            else:
                return JsonResponse(status=200, data={})
        else:
            return JsonResponse(status=400, data={})


@user_recruit_check
def join_chk(request):  # 회원 가입 페이지로 부터 정보를 받
    # POST로 데이터가 들어왔을 경우, 안들어 왔다면 -> 비정상 적인 접근임. 일반적으로 GET을 통해서는 접근이 불가능 해야함.
    if request.method == "POST":
        # 사용자 정보를 받아옴

        context = {  # 회원 가입 정보를 받아서 질문 폼으로 전송
            "user_role": request.POST.get("user_role"),
            "user_email": request.POST.get("user_email"),
            "user_major": request.POST.get("user_major"),
            "user_name": request.POST.get("user_name"),
            "user_stu": request.POST.get("user_stu"),
            "user_grade": int(request.POST.get("user_grade")),
            "user_phone": request.POST.get("user_phone"),
            "user_pic": request.POST.get("user_pic"),
            "provider": request.POST.get("provider"),
            "uid": request.POST.get("uid"),
            "quest_list": QuestForm.objects.all()
        }
        # 질문/답변 폼으로 보냄
        return render(request, "quest.html", context)

    return render(request, "index.html", {'lgn_is_failed': 1})


@user_recruit_check
def quest_chk(request):
    if request.method == "POST":  # POST로 데이터가 들어왔을 경우, 안들어 왔다면 -> 비정상적인 접근임. 일반적으로 GET을 통해서는 접근이 불가능 해야함.

        user_auth = 3
        user_role = 5 if request.POST.get("user_role") == "professor" else 6
        user_email = request.POST.get("user_email")
        user_major = MajorInfo.objects.filter(major_name=request.POST.get("user_major"))[0]
        user_name = request.POST.get("user_name")
        user_stu = request.POST.get("user_stu")
        user_grade = request.POST.get("user_grade")
        user_gen = UserSchedule.objects.get(pk=1).generation
        user_phone = request.POST.get("user_phone")
        user_pic = request.POST.get("user_pic")
        provider = request.POST.get("provider")
        uid = request.POST.get("uid")

        if UserSocialAccount.objects.filter(user_id=user_stu, provider=provider, uid=uid).count():  # 중복 방지
            session.save_session(request,
                                 user_model=User.objects.get(pk=user_stu),
                                 logined_email=user_email,
                                 provider=provider)
            return redirect("welcome")

        if user_pic is not None:
            try:  # 자신의 폴더가 남아 있을 경우의 예외처리
                os.mkdir(settings.MEDIA_ROOT + "/member/" + user_stu)
            except FileExistsError:
                pass
            try:  #
                if "png" in user_pic:
                    urlretrieve(user_pic, "/home/ibas/Django/IBAS/media/member/" + user_stu + "/" + user_stu + ".png")
                    user_pic = "member/" + user_stu + "/" + user_stu + ".png"
                elif "jpg" in user_pic:
                    urlretrieve(user_pic, "/home/ibas/Django/IBAS/media/member/" + user_stu + "/" + user_stu + ".jpg")
                    user_pic = "member/" + user_stu + "/" + user_stu + ".jpg"
                elif "gif" in user_pic:
                    urlretrieve(user_pic, "/home/ibas/Django/IBAS/media/member/" + user_stu + "/" + user_stu + ".gif")
                    user_pic = "member/" + user_stu + "/" + user_stu + ".gif"
                else:
                    user_pic = get_default_pic_path()
            except:
                user_pic = get_default_pic_path()

        with transaction.atomic():
            user = User.objects.create(
                user_name=user_name,  # 이름
                user_stu=user_stu,  # 학번
                user_grade=user_grade,  # 학년
                user_auth=get_object_or_404(UserAuth, pk=user_auth),  # 권한 번호
                user_gen=user_gen,  # 기수
                user_major=user_major,  # 전공
                user_role=get_object_or_404(UserRole, pk=user_role),  # 역할 정보
                user_phone=user_phone,  # 핸드폰 번호
                user_pic=user_pic  # 프로필 사진
            )
            UserSocialAccount.objects.create(
                email=user_email,
                provider=provider,
                user=user,
                uid=uid
            )
            if user_role == 6:  # 오직 일반 학생으로 가입했을 때만
                # 모든 질문 리스트를 뽑아옴: 질문이 몇번까지 있는지 알아야 답변을 몇번까지 했는지 알기 때문
                quest_list = QuestForm.objects.all()
                # 질문에 대한 답변을 저장하는 곳
                for quest in quest_list:
                    Answer.objects.create(
                        answer_quest=quest,
                        answer_cont=request.POST.get("answer_" + str(quest.quest_no)),
                        answer_user=user,
                    )
            session.save_session(request, user_model=user, logined_email=user_email, provider=provider)  # 로그인
            # 새로운 유저 가입을 회장단에게 알림.
            create_user_join_alarm(user)

        return redirect(reverse("welcome"))  # 정상 회원가입 완료시 회원 가입 완료 페이지로 이동.

    return render(request, "index.html", {'lgn_is_failed': 1})  # 비정상 적인 접근 시 로그인 실패 메시지 출력과 함께 메인페이지 이동.


def pass_param(request):  # 구글 로그인으로 부터 파라미터를 받아 넘기는 페이지, 사용자에겐 보이지 않음.
    return render(request, "pass_login_param.html", {})


def logout(request):  # 로그아웃
    request.session.clear()  # 세션 초기화
    return HttpResponseRedirect('/user/accounts/logout')  # 구글 세션 초기화 링크


def login(request):  # 로그인 페이지로 이동
    return render(request, 'login.html', {})


def welcome(request):  # 입부신청 완료 페이지로 이동
    return render(request, 'welcome.html', {})


def rulebook(request, type_no):  # 동아리 회칙 / 개인정보 이용 동의 사이트로 이동
    context = {
        "policy_terms": PolicyTerms.objects.filter(policy_type__type_no=type_no).order_by("-policy_updated").first()
    }
    return render(request, 'rulebook.html', context)

import os
from django.shortcuts import render, redirect, reverse
from DB.models import Board, User, Comment, Bank, UserUpdateRequest, UserEmail, StateInfo, MajorInfo, UserDelete, \
    ContestBoard, ContestComment, History, Answer, Lect, LectBoard, LectEnrollment, LectAttendance
from django.db.models import Q
from user_controller import get_logined_user, login_required, get_social_login_info, initialize_user, \
    get_default_pic_path, is_bank_related, is_history_related, is_default_pic, delete_all_infomation
from django.conf import settings
from member.session import save_session
from file_controller import FileController
import hashlib
from django.db import transaction


def get_ecrypt_value(value: str):
    return hashlib.md5(value.encode()).hexdigest()


# Create your views here.
@login_required
def my_info(request):  # 내 정보 출력
    context = {
        "my_board_list": Board.objects.filter(board_writer=get_logined_user(request)).order_by(
            "board_type_no").order_by("-board_created"),
        "my_comment_list": Comment.objects.filter(comment_writer=get_logined_user(request)).order_by(
            "comment_board_no__board_type_no").order_by("-comment_created"),
        "my_wait_request": UserUpdateRequest.objects.filter(
            Q(updated_user=get_logined_user(request)) & Q(updated_state__state_no=1)),
        "my_update_request_list": UserUpdateRequest.objects.filter(updated_user=get_logined_user(request)),
        "my_bank_list": Bank.objects.filter(bank_used_user=get_logined_user(request)).order_by("-bank_used"),
        "user_list": User.objects.all(),
        "major_list": MajorInfo.objects.all(),
        "is_naver_existed": len(
            UserEmail.objects.filter(Q(user_stu=get_logined_user(request)) & Q(provider="naver"))) != 0,
        "is_google_existed": len(
            UserEmail.objects.filter(Q(user_stu=get_logined_user(request)) & Q(provider="google"))) != 0,
    }
    return render(request, 'my_info.html', context)


def user_update_request_register(request):  # 이름 변경 신청
    if request.method == "POST":  # 포스트로 들어온 요청의 경우
        user_update_request = UserUpdateRequest.objects.create(  # 업데이트 신청 객체 생성
            updated_user_name=request.POST.get("updated_user_name"),
            updated_user=get_logined_user(request)  # 신청자: 로그인한 유저
        )
        user_update_request.save()  # 저장
    return redirect(reverse("my_info"))


# 유저 정보 수정 승인 거절 시 호출되는 함수.
def user_update_request_aor(request):
    if request.method == "POST":  # 포스트인가.
        updated_state = request.POST.get("updated_state")
        user_update_request = UserUpdateRequest.objects.get(pk=request.POST.get("updated_no"))

        # 승인 거절의 경우
        if updated_state == 2:
            user_update_request.updated_reject_reason = request.POST.get("updated_reject_reason")

        # 승인할 경우
        else:
            # 유저 이름 수정 반영
            user = user_update_request.updated_user
            user.user_name = user_update_request.updated_user_name
            user.save()

        user_update_request.updated_state = StateInfo.objects.get(pk=updated_state)  # 상태 업로드
        user_update_request.save()

    return redirect(reverse("my_info"))


def user_pic_update(request):
    if request.method == "POST":
        user_pic = request.FILES.get("user_pic")
        user = get_logined_user(request)
        if user_pic is not None:
            if not is_default_pic(user.user_pic):  # 만약 사용자의 이미지가 디폴트 이미지가 아니라면
                try:
                    os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))  # 프  로필 이미지 삭제
                except FileNotFoundError:
                    pass
            # 새로운 이미지로 교체.
            user.user_pic = user_pic
            user.save()
    return redirect(reverse("my_info"))


@login_required
def user_pic_delete(request):
    user = get_logined_user(request)
    if not is_default_pic(user.user_pic):  # 기존에 있던 사진이 디폴트 사진이 아닌 경우.
        try:
            os.remove(settings.MEDIA_ROOT + "/" + str(user.user_pic))  # 이전 파일 삭제
        except FileNotFoundError:
            pass
    user.user_pic = get_default_pic_path()
    user.save()
    return redirect(reverse("my_info"))


@login_required
def user_major_update(request):
    current_user = get_logined_user(request)
    if len(MajorInfo.objects.filter(major_name=request.POST.get("user_major"))) != 0:
        current_user.user_major = MajorInfo.objects.filter(major_name=request.POST.get("user_major")).first()
        current_user.save()
    return redirect(reverse("my_info"))


@login_required
def user_phone_update(request):
    if request.method == "POST":
        current_user = get_logined_user(request)
        current_user.user_phone = request.POST.get("user_phone")
        current_user.save()
        return redirect(reverse("my_info"))
    else:
        return redirect(reverse("index"))


# 연동시 파라미터를 남기기 위한 코드 (GET 방식이기 때문에 보안에 매우 취약함.)
def go_social_login_before_setting(request):
    if request.method == "POST":
        encoded_user_stu = get_ecrypt_value(str(get_logined_user(request).user_stu))
        context = {
            "provider": request.POST.get("provider"),
            "next_url": "/user/pass?user_stu=" + encoded_user_stu,
        }
        return render(request, "go_social_login.html", context)
    return redirect(reverse("index"))


# login_required를 설정하지 말 것. 연동시 로그인이 잠시 풀리기 때문.
def connect_social_account(request):
    if request.method == "POST":
        social_dict = get_social_login_info(request.POST.get("password"))
        target_user_stu = request.POST.get("user_stu")
        current_user = None
        for user in User.objects.all():
            if target_user_stu == get_ecrypt_value(str(user.user_stu)):
                current_user = user
                break

        if current_user is not None:
            UserEmail.objects.create(user_stu=current_user, user_email=social_dict.get("email"),
                                     provider=social_dict.get("provider"))
            save_session(request, user_model=current_user, logined_email=social_dict.get("email"),
                         provider=social_dict.get("provider"))
            return redirect(reverse("my_info"))
    return redirect(reverse("index"))


# 회원 탈퇴 시 실행되는 함수,.
@login_required
def withdrawal(request):
    if request.method == "POST":
        if User.objects.get(pk=request.POST.get("user_stu")) == get_logined_user(request) and not get_logined_user(
                request).user_role.role_no <= 4:
            if bool(request.POST.get("agreement")):
                with transaction.atomic():
                    current_user = get_logined_user(request)
                    # 회계를 요청한 유저거나, 회계를 작성한 유저, 연혁을 작성한 유저의 경우 데이터 무결성을 위해 최소한의 개인정보 만을 남기고 초기화시킴
                    if is_bank_related(current_user) or is_history_related(current_user):
                        initialize_user(current_user)  # 유저 정보 초기화
                        delete_all_infomation(current_user)  # 유저 정보 삭제
                    # 회계나 연혁에 관련 없는 계정의 경우 DB에서 계정 완전 삭제
                    else:
                        FileController.delete_all_files_of_(current_user)
                        current_user.delete()
                    return redirect("logout")  # 최후의 로그아웃 (세션 제거용)
    # 비정상적인 접근의 경우(해킹 시도)
    return redirect(reverse("my_info"))  # 내 정보 페이지로 이동.

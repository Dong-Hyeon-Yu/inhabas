import os

from django.shortcuts import render, redirect, reverse
from DB.models import Board, User, Comment, Lect, LectBoard, BoardType, UserRole, Bank, UserAuth, UserUpdateRequest, \
    UserEmail, \
    StateInfo, MajorInfo, AuthUser
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.db.models import Q
from user_controller import get_logined_user, get_user, is_logined, login_required
from django.conf import settings


# Create your views here.

@login_required
def my_info(request):  # 내 정보 출력
    context = {
        "my_board_list": Board.objects.filter(board_writer=get_logined_user(request)).order_by(
            "board_type_no").order_by(
            "-board_created"),
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


def get_default_pic_path():
    return "member/default/default.png"


def is_default_pic(img_path):
    return str(img_path) == get_default_pic_path()


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


# @login_required
# def connect_social_login(request):
#     if request.method == "POST":


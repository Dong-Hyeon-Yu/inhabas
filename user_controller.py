import functools
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from DB.models import User, ContestBoard, Board, Bank, Lect, UserDelete, AuthUser, History, LectEnrollment, \
    ContestComment, LectBoard, Answer, UserEmail, Comment, LectAssignmentSubmit, Alarm
from allauth.socialaccount.models import SocialAccount, SocialToken
from file_controller import FileController
from django.db.models import Q
from django.db import transaction


# 학교 아이디의 경우 이름/학과/학교 등으로 이름이 구성된 경우가 많음.
# 그 경우 앞부분을 잘라주는 함수임.
def get_real_name(name_str: str):
    real_name = name_str
    idx_slash = name_str.find("/")
    if idx_slash != -1:
        real_name = name_str.split("/")[0]
    return real_name


# 소셜로그인으로부터 정보를 얻어오는 함수임
def get_social_login_info(password):
    auth_user = AuthUser.objects.filter(password=password).first()
    # 있다면 social account에서 앞서서 Auth의 primary key를 통해 가입한 친구의 pk를 넣어서 조회
    tar_member = SocialAccount.objects.filter(user_id=auth_user.id).first()  # quesyset의 첫번째 자료. 즉 로그인한 인원의 인스턴스 변수
    tar_token = SocialToken.objects.filter(account_id=tar_member.id).first()
    social_login_info_dict = dict()

    # extra_data: 사용자의 동의를 통해 로그인 출처로 부터 얻은 사용자의 개인정보
    social_login_info_dict["email"] = tar_member.extra_data.get('email')  # 자동 완성을 위해 인스턴스 변수 설정
    social_login_info_dict["name"] = get_real_name(tar_member.extra_data.get('name'))  # 자동 완성을 위한 이름 설정
    social_login_info_dict["provider"] = tar_member.provider
    if social_login_info_dict["provider"] == "google":  # 사용자가 구글을 통해 로그인 한 경우
        social_login_info_dict["pic"] = tar_member.extra_data.get('picture')  # extra_data 테이블에서 꺼내는 변수를 picture로 설정
    elif social_login_info_dict["provider"] == "naver":  # 사용자가 네이버를 통해 로그인 한 경우
        social_login_info_dict["pic"] = tar_member.extra_data.get(
            'profile_image')  # extra_data 테이블에서 꺼내는 변수를 profile_image로 설정

    # 소셜 로그인으로 부터 받은 정보는 저장하지 않기 위해 해당 정보 삭제
    tar_token.delete()
    tar_member.delete()
    auth_user.delete()

    return social_login_info_dict


# 로그인 했는지 여부를 반환하는 함수
def is_logined(request):
    return request.session.get("user_stu") is not None


# 관리자인지의 여부를 확인하는 함수
def is_superuser(request):
    current_user = get_logined_user(request)
    return current_user.user_role.role_no <= 3


# 글쓴이인지의 여부를 확인하는 함수
def is_writer(request, **kwargs):
    current_user = get_logined_user(request)
    board_no = kwargs.get('board_no')
    contest_no = kwargs.get('contest_no')
    bank_no = kwargs.get('bank_no')
    lect_no = kwargs.get('lect_no', kwargs.get('room_no'))
    user_delete_no = kwargs.get('user_delete_no')
    assignment_submit_no = kwargs.get('submit_no')  # 수강생 과제 제출

    # comment_no = kwargs.get('comment_no')

    # 글쓴이인가요
    if board_no is not None:
        board = Board.objects.get(pk=board_no)
        if current_user == board.board_writer:
            return True
    elif contest_no is not None:
        contest = ContestBoard.objects.get(pk=contest_no)
        if current_user == contest.contest_writer:
            return True
    elif assignment_submit_no is not None:
        assignment = LectAssignmentSubmit.objects.get(pk=assignment_submit_no)
        if current_user == assignment.assignment_submitter:
            return True
    elif lect_no is not None:
        lect = Lect.objects.get(pk=lect_no)
        if current_user == lect.lect_chief:
            return True
    elif bank_no is not None:
        bank = Bank.objects.get(pk=bank_no)
        if current_user == bank.bank_used_user:
            return True
    elif user_delete_no is not None:
        user_delete = UserDelete.objects.get(pk=user_delete_no)
        if current_user == user_delete.suggest_user:
            return True
    else:
        return False


# 역할이 맞는지 확인 하는 함수
def role_check(request, role_no):
    return get_logined_user(request).user_role.role_no == role_no


#
# # 권한이 맞는지 확인하는 함수
# def auth_check(request, auth_no):
#     return get_logined_user(request).user_auth.auth_no == auth_no


# 유저 관련 객체를 반환하는 컨트롤러
def get_logined_user(request):  # 로그인한 유저 객체 반환
    return User.objects.get(pk=request.session.get("user_stu"))


# 학번을 넣어서 조회할 경우
def get_user(user_stu):
    return User.objects.get(pk=user_stu)


# post를 사용해서 일반적으로 받아온 경우
def get_user_post(request):
    return User.objects.get(pk=request.POST.get("user_stu"))


# get를 사용해서 일반적으로 받아온 경우
def get_user_get(request):
    return User.objects.get(pk=request.GET.get("user_stu"))


# 작성자: 유동현
# 작성일시 : 2021.07.14
# 잘못된 접근시 메인페이지로 이동시킴
# msg 에 메세지를 적으면, 메인페이지에서 alert 창으로 경고를 띄움 (default msg = '접근 권한이 없습니다.')
# 차라리 조용히 404 페이지를 띄워주는것도 좋을거같고..? => 해당 url 이 존재하는지 외부로부터 감출 수 있음
def not_allowed(request, msg="접근 권한이 없습니다.", error_404=False):
    if error_404:
        raise Http404
    else:
        messages.warning(request, msg)  # 메인에서 alert 창 띄우기
        return redirect(reverse("index"))


# 데코레이터
# 로그인 안한 유저가 접근시 메인페이지로 이동
def login_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if is_logined(request):
            return func(request, *args, **kwargs)
        else:
            return not_allowed(request, msg='로그인이 필요합니다!')

    return wrapper


# 데코레이터
# 작성자: 유동현
# 수정자: 양태영
# 현재 접속 중인 유저가 글쓴이인지 확인하는 함수, 글을 수정 및 삭제할 때 필요
# superuser=True 이면 관리자 모드. 관리자인 경우도 접근 허용
# superuser=False 이면 관리자도 접근 불가. 글쓴이만 접근 가능
# 수정내용: 체크 부분 모듈화로 코드 간결화
def writer_only(superuser=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            # 권한이 일치하지 않으면 메인페이지로 이동
            if superuser:
                if is_writer(request, **kwargs) or is_superuser(request):
                    return func(request, *args, **kwargs)
            else:
                if is_writer(request, **kwargs):
                    return func(request, *args, **kwargs)

            return not_allowed(request, error_404=True)

        return wrapper

    return decorator


# 데코레이터
# 수정자:양태영
# 수정일시: 6월 16일
# 수정내용: 총무 권한을 추가할지 추가하지 않을지 결정하는 함수. True일 경우 총무여도 권한 허용.
# 관리자 권한이 있는지 확인하는 함수
def superuser_only(cfo_included=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            current_user = get_logined_user(request)
            flag = 3
            if cfo_included:
                flag = 4
            if current_user.user_role.role_no <= flag:
                return func(request, *args, **kwargs)
            else:
                return not_allowed(request, error_404=True)

        return wrapper

    return decorator


# 데코레이터
# 총무 권한이 있는지 확인하는 함수
def cfo_only(func):
    @login_required
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        current_user = get_logined_user(request)

        if current_user.user_role.role_no == 4:
            return func(request, *args, **kwargs)

        else:
            return not_allowed(request, error_404=True)

    return wrapper


# 데코레이터
# 사용자 권한을 확인하는 함수(활동회원 or 비활동회원)
# 전체 회원 중 일원인지만 확인할 경우: active=False
# 납입 회원인지 확인할 경우: active=True
def auth_check(active=False):
    def decorator(func):
        @login_required
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            current_user = get_logined_user(request)
            if active:
                boundary = current_user.user_auth.auth_no == 1
            else:
                boundary = current_user.user_auth.auth_no <= 2

            if boundary:
                return func(request, *args, **kwargs)
            else:
                return not_allowed(request)

        return wrapper

    return decorator


# 데코레이터
# 제작일: 21.6.21 15.43
# 제작자: 양태영
# 용도: 회장인지 아닌지 판별하는 데코레이터 vice가 True 일 경우 부화장인지 봄
def chief_only(vice=False):
    def decorator(func):
        @login_required
        @auth_check(True)
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            current_user = get_logined_user(request)
            if vice and current_user.user_role.role_no <= 2:
                return func(request, *args, **kwargs)
            elif not vice and current_user.user_role.role_no == 1:
                return func(request, *args, **kwargs)
            else:
                return not_allowed(request, error_404=True)

        return wrapper

    return decorator


# 데코레이터
# 제작일: 21.7.13
# 제작자: 유동현
# 용도: 강의 또는 스터디 구성원인지 확인하는 용도
def member_only(func):
    @login_required
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        current_user = get_logined_user(request)
        lect_room = Lect.objects.prefetch_related(
            'enrolled_students').get(pk=kwargs.get('room_no', kwargs.get('lect_no')))
        if current_user == lect_room.lect_chief:
            return func(request, *args, **kwargs)
        elif member := lect_room.enrolled_students.filter(lect_no=lect_room, student=current_user).first():
            if member.status_id == 1:
                return func(request, *args, **kwargs)

        return not_allowed(request, msg='수강정지 되었거나, 접근할 수 없는 멤버입니다!')

    return wrapper


# 디폴트 프로필 사진의 경로를 얻어옴
def get_default_pic_path():
    return "member/default/default_profile.png"


# 기존의 이미지 패스가 디폴트 패스인지 검사
def is_default_pic(img_path):
    return str(img_path) == get_default_pic_path()


# # ------------ deprecated -------------
# # 삭제 사유: 관리하기 불편함. is_related(user) 함수를 사용할 것.
# # 활동 게시판과 유저가 관련되어 있는지 확인하는 함수
# def is_activity_related(user: User):
#     return len(Board.objects.filter(Q(board_writer=user) & Q(board_type_no__board_type_no=4))) != 0
#
#
# # 공모전 게시판과 유저가 관련되어 있는지 확인하는 함수.
# def is_contest_related(user: User):
#     return len(ContestBoard.objects.filter(contest_writer=user)) != 0
#
#
# # 회계와 관련되어있는지 확인하는 함수
# def is_bank_related(user: User):
#     return len(Bank.objects.filter(Q(bank_cfo=user) | Q(bank_used_user=user))) != 0
#
#
# # 연혁과 관련되어있는지
# def is_history_related(user: User):
#     return len(History.objects.filter(history_writer=user)) != 0
# ---------------------------------------


# 초기화를 할지 삭제를 할 지 결정하는 함수
def is_related(user: User):
    # 활동 게시판이랑 관련이 있는가?
    if len(Board.objects.filter(Q(board_writer=user) & Q(board_type_no__board_type_no=4))) != 0:
        return True
    # 공지 사항과 관련이 있는가?
    if len(Board.objects.filter(Q(board_writer=user) & Q(board_type_no__board_type_no=1))) != 0:
        return True
    # 공모전 게시판이랑 관련이 있는가?
    if len(ContestBoard.objects.filter(contest_writer=user)) != 0:
        return True
    # 예산 지원신청을 하였거나, 예산을 처리한 적이 있는가?
    if len(Bank.objects.filter(Q(bank_cfo=user) | Q(bank_used_user=user))) != 0:
        return True
    # 연혁에 개입하였는가?
    if len(History.objects.filter(history_writer=user)) != 0:
        return True
    return False


# 최소한의 개인정보(학번, 유저 이름)만 남기고 모든 정보를 초기화시키는 함수.
# IN: 초기화시킬 User 인스턴스
# OUT: 초기화시킨 User 인스턴스
def initialize_user(user: User):
    user.user_auth = None
    user.user_role = None
    user.user_phone = None
    user.user_major = None
    user.user_gen = None
    user.user_grade = None
    user.user_pic = get_default_pic_path()
    return user.save()


# 계정 초기화를 하면 모든 게시글이 사라지지 않으므로 자신과 연관된 모든 데이터를 지우는 함수.
def delete_all_infomation(user: User):
    # 본인 게시글 삭제(단 활동 게시판의 게시글은 공익을 위한 게시글이므로 삭제되어선 안된다.)
    my_board_list = Board.objects.filter(
        Q(board_writer=user) & ~Q(board_type_no__board_type_no=4) & ~Q(board_type_no__board_type_no=1))
    for my_board in my_board_list:
        FileController.delete_all_files_of_(my_board)
        my_board.delete()

    # 본인 덧글 삭제
    my_comment_list = Comment.objects.filter(
        Q(comment_writer=user) | Q(comment_cont_ref__comment_writer=user))
    for my_comment in my_comment_list:
        my_comment.delete()

    # ------------ deprecated -------------
    # 삭제사유: 공모전 게시글은 공익을 위한 게시글이므로 삭제되어선 안된다.
    # # 본인 공모전 글 삭제
    # my_contest_list = ContestBoard.objects.filter(contest_writer=user)
    # for my_contest in my_contest_list:
    #     FileController.delete_all_files_of_(my_contest)
    #     my_contest.delete()
    # -------------------------------------

    # 본인 공모전 덧글 삭제
    my_contest_comment_list = ContestComment.objects.filter(
        Q(comment_writer=user) | Q(comment_cont_ref__comment_writer=user))
    for my_contest_comment in my_contest_comment_list:
        my_contest_comment.delete()

    # 본인이 제명 대상자로 있거나, 본인이 발안한 제명 안건 삭제
    my_user_delete_list = UserDelete.objects.filter(
        Q(suggest_user=user) | Q(deleted_user=user))
    for my_user_delete in my_user_delete_list:
        FileController.delete_all_files_of_(my_user_delete)
        my_user_delete.delete()

    # 본인이 작성한 강의실 게시글 삭제
    my_lect_board_list = LectBoard.objects.filter(lect_board_writer=user)
    for my_lect_board in my_lect_board_list:
        FileController.delete_all_files_of_(my_lect_board)
        my_lect_board.delete()

    # 본인이 수강중인 강의 삭제
    my_lect_enrollment_list = LectEnrollment.objects.filter(student=user)
    for my_lect_enrollment in my_lect_enrollment_list:
        my_lect_enrollment.delete()

    # 본인이 개설한 강의/스터디/취미모임 삭제
    my_lect_list = Lect.objects.filter(lect_chief=user)
    for my_lect in my_lect_list:
        FileController.delete_all_files_of_(my_lect)
        my_lect.delete()

    # 연동한 이메일 모두 삭제
    my_email_list = UserEmail.objects.filter(user_stu=user)
    for my_email in my_email_list:
        my_email.delete()

    # 가입 질문에 대한 답변 모두 삭제
    my_answer_list = Answer.objects.filter(answer_user=user)
    for my_answer in my_answer_list:
        my_answer.delete()
    # 본인 계정 프로필 사진 삭제
    if not is_default_pic(str(user.user_pic)):
        FileController.delete_all_files_of_(user)

    my_alarm_list = Alarm.objects.filter(alarm_user=user)
    for my_alarm in my_alarm_list:
        my_alarm.delete()



# 삭제 로직
def delete_user(user: User):
    if not user.user_role.role_no <= 4:
        with transaction.atomic():
            # 회계를 요청한 유저거나, 회계를 작성한 유저, 연혁을 작성한 유저, 활동 게시판 게시글을 작성한 유저,
            # 공모전 게시판의 게시글을 작성한 유저의 경우 데이터 무결성을 위해 최소한의 개인정보 만을 남기고 초기화시킴
            if is_related(user):
                initialize_user(user)  # 유저 정보 초기화
                delete_all_infomation(user)  # 유저의 게시글 및 흔적 모두 삭제
            # 회계나 연혁에 관련 없는 계정의 경우 DB에서 계정 완전 삭제

            else:
                if not is_default_pic(str(user.user_pic)):  # 프로필 사진인 디폴트 사진이 아닌 경우
                    FileController.delete_all_files_of_(user)  # 데이터 베이스에서 삭제함
                user.delete()
            return True
    return False




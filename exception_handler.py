from django.contrib import messages
from DB.models import Lect, Board, LectBoard, ContestBoard
from django.shortcuts import redirect, reverse


# 에러메시지를 얻는 함수.
def get_error_message(request, name="게시글이"):
    messages.warning(request, f'해당 {name} 존재하지 않습니다. 삭제되었을 수 있습니다.')


### 각 인스턴스가 존재하는지 확인하고 존재하면 인스턴스를, 존재하지 않으면 에러메시지를 출력 후 리스트 페이지로 돌아가는 함수.

def lect_exist_check(request, lect_no):
    try:
        Lect.objects.get(pk=lect_no)
    except Lect.DoesNotExist:
        get_error_message(request, "강의가")
        return redirect("lect_view", type_no=1)


def lect_board_exist_check(request, lect_board_no, room_no):
    try:
        LectBoard.objects.get(pk=lect_board_no)
    except LectBoard.DoesNotExist:
        get_error_message(request)
        return redirect("lect_room_main", room_no=room_no)

def board_exist_check(request, board_no):
    try:
        Board.objects.get(pk=board_no)
    except Board.DoesNotExist:
        get_error_message(request)
        return redirect("board_view", board_type_no=5)

def contest_board_exist_check(request, contest_no):
    try:
        ContestBoard.objects.get(pk=contest_no)
    except ContestBoard.DoesNotExist:
        get_error_message(request)
        return redirect(reverse("contest_list"))


def activity_exist_check(request, board_no):
    try:
        Board.objects.get(pk=board_no)
    except Board.DoesNotExist:
        get_error_message(request)
        return redirect("activity")

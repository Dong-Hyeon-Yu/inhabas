from django.db import transaction
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, reverse, redirect
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History, Bank, BankFile, BankApplyInfo  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from bank.forms import BankForm, FileForm, BankSupportForm
from date_controller import today
from file_controller import FileController
from pagination_handler import get_page_object
from user_controller import get_logined_user, writer_only, cfo_only, auth_check, not_allowed
from alarm.alarm_controller import create_bank_alarm


@auth_check()
def bank(request):
    # 회계 내역
    bank_list = Bank.objects.filter(bank_apply__bank_apply_no=4).order_by('-bank_used').prefetch_related('files').all()

    # 연도를 담을 리스트
    year_list = [bank.bank_used.year for bank in bank_list]
    year_list = list(set(year_list))
    year_list.sort()

    # 수입, 지출 합계
    total_income = Bank.objects.filter(bank_apply__bank_apply_no=4).aggregate(Sum("bank_plus"))["bank_plus__sum"]
    total_outcome = Bank.objects.filter(bank_apply__bank_apply_no=4).aggregate(Sum("bank_minus"))["bank_minus__sum"]
    if total_income is None:
        total_income = 0
    if total_outcome is None:
        total_outcome = 0
    balance = total_income - total_outcome

    # 페이지네이션 설정
    bank_list = get_page_object(request, bank_list, 15)  # 페이지네이션 15개씩 보이게 설정

    # 폼 객체
    bank_form = BankForm()
    file_form = FileForm()
    context = {
        "bank_list": bank_list,
        "year_list": year_list,
        "balance": balance,
        'bank_form': bank_form,
        'file_form': file_form,
    }

    return render(request, 'bank_list.html', context)


@cfo_only
def bank_delete(request, bank_no):
    if request.method == "POST":  # 포스트로 넘어오는 경우
        bank = get_object_or_404(Bank, pk=bank_no)
        FileController.delete_all_files_of_(bank)
        bank.delete()  # 파일과 폴더 삭제 후, 회계 DB 에서 삭제

        return redirect(reverse('bank_list'))

    return redirect(reverse("index"))


@cfo_only
def bank_update(request, bank_no):
    if request.method == "POST":
        bank = get_object_or_404(Bank, pk=bank_no)
        bank_form = BankForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if bank_form.is_valid():  # 새로 올라온 파일이 있는 경우
            bank_form.update(instance=bank)
            bank_files = BankFile.objects.filter(file_fk=bank)  # 게시글 파일을 불러옴
            FileController.update_file_by_file_form(request=request, instance=bank, files=bank_files,
                                                    file_form=file_form, required=True)
        return redirect(reverse('bank_list'))
    else:  # 비정상적인 접근의 경우 (해킹시도)
        return redirect(reverse("index"))  # 메인페이지로 보내버림


@cfo_only
def bank_register(request):
    if request.method == "POST":
        bank_form = BankForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if bank_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                bank = bank_form.save(bank_cfo=get_logined_user(request))
                file_form.save(instance=bank)
        else:
            pass  # 오류처리 필요

        return redirect(reverse('bank_list'))

    else:
        return redirect(reverse("index"))


@auth_check(active=True)
def bank_support_board(request):
    bank_list = Bank.objects.filter(~Q(bank_apply__bank_apply_no=4))

    # 페이지네이터 설정
    bank_list = get_page_object(request, bank_list, 15)  # 페이지네이션 15개씩 보이게 설정

    context = {
        "bank_list": bank_list,
    }

    return render(request, 'bank_support_board.html', context)  # 게시판 목록


@auth_check(active=True)
def bank_support_register(request):
    if request.method == "POST":
        bank_support_form = BankSupportForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if bank_support_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                bank = bank_support_form.save(user=get_logined_user(request))
                file_form.save(instance=bank)
                create_bank_alarm(bank)
        return redirect("bank_support_detail", bank_no=bank.bank_no)

    elif request.method == 'GET':
        context = {
            'bank_support_form': BankSupportForm(),
            'file_form': FileForm()
        }
        return render(request, 'bank_support_register.html', context)


@auth_check(active=True)
def bank_support_detail(request, bank_no):
    bank = get_object_or_404(Bank, pk=bank_no)
    bank_file_list = BankFile.objects.filter(file_fk=bank)
    context = {
        "bank": bank,
        "bank_file_list": bank_file_list
    }
    return render(request, 'bank_support_detail.html', context)  # 상세보기


@cfo_only
def bank_support_aor(request, bank_no):  # 총무가 승인, 승인거절, 지급완료를 눌렀을 때의 과정
    if request.method == "POST":
        bank = Bank.objects.get(pk=bank_no)
        bank_apply_no = int(request.POST.get("bank_apply_no"))
        bank.bank_apply = BankApplyInfo.objects.get(pk=bank_apply_no)
        bank.bank_cfo = get_logined_user(request)
        if bank_apply_no == 2:  # 승인 시
            bank.bank_checked = today()  # 검토일, 오늘
        elif bank_apply_no == 3:  # 거절 시
            bank.bank_checked = today()  # 검토일, 오늘
            bank.bank_reject_reason = request.POST.get("bank_reject_reason")
        elif bank_apply_no == 4:  # 지급 완료 시
            bank.bank_allowed = today()  # 지급 완료일, 오늘
        bank.save()
        return redirect("bank_support_detail", bank_no=bank_no)

    else:
        return redirect(reverse("bank_support_board"))


@writer_only()
def bank_support_update(request, bank_no):
    bank = get_object_or_404(Bank, pk=bank_no)
    if bank.bank_apply.bank_apply_no <= 2:
        return not not_allowed(request=request, msg="거절되었거나, 처리 완료된 예산 지원 신청입니다.\n\n수정이 불가능합니다.", error_404=False,
                               next_url="my_info")
    # ???
    # if request.POST.get("is_move") is not None:  # 단순 수정페이지 이동의 경우
    if request.method == "GET":
        context = {
            "bank_no": bank_no,
            "bank_file_list": BankFile.objects.filter(file_fk=bank),
            "bank_support_form": BankSupportForm(instance=bank),
            "file_form": FileForm(),
        }
        return render(request, "bank_support_register.html", context)

    elif request.method == "POST":  # 수정을 한 후 수정 버튼을 사용자가 눌렀을 경우
        bank_support_form = BankSupportForm(request.POST)
        file_form = FileForm(request.POST, request.FILES)

        if bank_support_form.is_valid() and file_form.is_valid():
            with transaction.atomic():
                bank_support_form.update(instance=bank)
                bank_file_list = BankFile.objects.filter(file_fk=bank)
                FileController.remove_files_by_user(request, bank_file_list)
                file_form.save(instance=bank)

            return redirect("bank_support_detail", bank_no=bank_no)

    return redirect(reverse("bank_support_board"))


@writer_only(superuser=True)
def bank_support_delete(request, bank_no):  # 예산지원 삭제
    if request.method == "POST":  # 포스트로 넘어오는 경우
        bank = get_object_or_404(Bank, pk=bank_no)
        if bank.bank_apply.bank_apply_no == 4:
            return not not_allowed(request=request, msg="예산 지원 신청이 이미 회계에 반영되었습니다.\n\n삭제를 원하시면 총무에게 문의하세요.", error_404=False,
                                   next_url="my_info")
        FileController.delete_all_files_of_(bank)  # 로컬 파일 삭제
        bank.delete()  # 파일과 폴더 삭제 후, 회계 DB 에서 삭제

    # 삭제 성공 유무와 상관없이 이동.
    return redirect(reverse('bank_support_board'))  # 예산 지원 신청 게시판으로 이동

from django.shortcuts import render, get_object_or_404, reverse, redirect
from allauth.socialaccount.models import SocialAccount  # 소셜 계정 DB, socialaccount_socialaccount 테이블을 사용하기 위함.
from DB.models import AuthUser, User, ChiefCarrier, UserRole, Board, BoardFile, \
    BoardType, Comment, History, Bank, BankFile  # 전체 계정 DB, AuthUser 테이블을 사용하기 위함.
from member import session
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.conf import settings
from IBAS.user_controller import is_chief_exist, is_sub_chief_exist, get_sub_chief, get_chief
import os
from IBAS.file_controller import get_filename, get_filename_with_ext


# Create your views here.
# 동아리 소개 작업할 것임
def bank_board(request):
    bank_list = Bank.objects.order_by('-bank_created').prefetch_related('bankfile_set')
    sum_list = list()
    for i in range(len(bank_list)):
        if i == 0:
            sum_list = bank_list[i].bank_plus - bank_list[i].bank_minus
        else:
            sum_list.append(sum_list[i] + bank_list[i].bank_plus - bank_list[i].bank_minus)
    year_list = list()
    for bank in bank_list:
        year_list.append(str(bank.bank_created).split('-')[0])

    year_list = list(set(year_list))
    year_list.sort()

    context = {
        "bank_list": bank_list,
        "year_list": year_list,
        "sum_list": sum_list
    }
    return render(request, 'bank_board.html', context)


def bank_delete(request):
    if request.method == "POST":
        bank = Bank.objects.get(pk=request.POST.get("bank_no"))  # 가져온 bank_no 사용
        bank.delete()
        return redirect(reverse("bank_board"))  # 뱅크 페이지로 리다이렉팅
    else:
        return render(request, "index.html", {'lgn_is_failed': 1})  # 메인페이지로 보내버림


def bank_update(request):
    if request.method == "POST":
        bank = Bank.objects.get(pk=request.POST.get("bank_no"))
        bank.bank_created = request.POST.get('bank_created')
        bank.bank_title = request.POST.get('bank_title')
        bank.bank_plus = request.POST.get('bank_plus')
        bank.bank_minus = request.POST.get('bank_minus')
        bank.save()
        return redirect(reverse('bank_board'))
    else:  # 비정상적인 접근의 경우 (해킹시도)
        return render(request, "index.html", {'lgn_is_failed': 1})  # 메인페이지로 보내버림


def bank_register(request):
    if request.method == "POST":
        bank = Bank(
            bank_created=request.POST.get('bank_created'),
            bank_title=request.POST.get('bank_title'),
            bank_plus=request.POST.get('bank_plus'),
            bank_minus=request.POST.get('bank_minus'),
            # cfo는 승인하는 사람인데, 처음 등록할 땐 아직 승인한 사람이 없어서 신청한 사람으로 받았음
            bank_cfo=User.objects.get(pk=request.session.get('user_stu')),
            # 사용한 사람은 user_stu 임
            bank_used_user=User.objects.get(pk=request.session.get('user_stu')),
            bank_apply=request.POST.get('bank_apply')
        )
        bank.save()

        for updated_file in request.FILES.getlist('bank_file'):
            new_bank_file = BankFile.objects.create(bank_no=Bank.objects.get(pk=bank.bank_no),
                                                    bank_file_path=updated_file)
            new_bank_file.save()
        return redirect(reverse('bank_board'))
    else:
        return render(request, "index.html", {'lgn_is_failed': 1})

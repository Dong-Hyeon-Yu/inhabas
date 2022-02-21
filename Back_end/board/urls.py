from django.urls import path
from . import views

urlpatterns = [
    path('<int:board_type_no>', views.board_view_wrapper, name="board_view"),  # 게시판페이지로 이동
    path('detail/<int:board_no>/', views.detail_view_wrapper, name="board_detail"),  # 게시판 상세게시판으로 이동
    path('search/<int:board_type_no>', views.board_search, name="board_search"),
    path('register/', views.board_register, name="board_register"),
    path('update/<int:board_no>/', views.board_update, name="board_update"),
    path('delete/<int:board_no>/', views.board_delete, name="board_delete"),


    # 공모전 게시판
    path('contest', views.contest_view, name="contest_list"),  # 공모전 게시판페이지로 이동
    path('contest/register', views.contest_register, name="contest_register"),  # 공모전 게시판 등록페이지로 이동
    path('contest/detail/<int:contest_no>', views.contest_detail, name="contest_detail"),  # 공모전 게시판 상세보기페이지로 이동
    path('contest/delete/<int:contest_no>', views.contest_delete, name="contest_delete"),
    path('contest/update/<int:contest_no>', views.contest_update, name="contest_update"),
    path('contest/search/', views.contest_search, name="contest_search"),

]

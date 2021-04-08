from django.urls import path, include
from . import views

# Media files 저장 및 전달 설정하기 위한 import
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("member/list/", views.staff_member_list, name="staff_member_list"), # 이거 뭐죠 백앤드가 작업 하지 않은 거면 삭제해야함
    path("member/update/", views.staff_member_update, name="staff_member_update"), # 이거 뭐죠 백앤드가 작업 하지 않은 거면 삭제해야함
    path('member/delete/list/', views.member_delete_list, name='member_delete_list'),
   path('member/delete/detail/', views.member_delete_detail, name='member_delete_detail'),
   path('member/delete/register/', views.member_delete_register, name='member_delete_register'),
    path('member/applications/', views.member_applications, name='member_applications'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
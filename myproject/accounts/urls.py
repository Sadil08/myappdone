from django.contrib import admin
from django.urls import path
from . import views
from .views import search_teachers
from .views import request_teacher, admin_teacher_requests, approve_teacher_request
from .views import confirm_time, decline_time, delete_teacher
from .views import forum_subjects, forum_by_subject, question_detail, upload_paper

urlpatterns = [
    path('register/student/', views.student_register, name='student_register'),
    path('register/teacher/', views.teacher_register, name='teacher_register'),
    path('register/admin/', views.admin_register, name='admin_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-teacher/<int:teacher_id>/', views.approve_teacher, name='approve_teacher'),
    path('search-teachers/', views.search_teachers, name='search_teachers'),
    path('request-teacher/<int:teacher_id>/', views.request_teacher, name='request_teacher'),
    path('admin-dashboard/teacher-requests/', views.admin_teacher_requests, name='admin_teacher_requests'),
    path('admin-dashboard/teacher-requests/approve/<int:request_id>/', views.approve_teacher_request, name='approve_teacher_request'),
    path('admin-dashboard/teacher-overview', views.admin_teacher_overview, name = 'admin_teacher_overview'),
    path('schedule/<int:schedule_id>/confirm/', confirm_time, name='confirm_time'),
    path('schedule/<int:schedule_id>/decline/', decline_time, name='decline_time'),
    path('', views.home, name='home'),
    path('aboutus/', views.about_us, name='about_us'),
    path('delete-teacher/<int:teacher_id>/', delete_teacher, name='delete_teacher'),
    path('submit-review/<int:teacher_id>/', views.submit_review, name='submit_review'),
    path('forum/', views.forum_subjects, name='forum_subjects'),
    path('forum/<int:subject_id>/', views.forum_by_subject, name='forum_by_subject'),
    path('forum/question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('upload-paper/', upload_paper, name='upload_paper'),

    
]






from django.urls import path
from . import views

urlpatterns = [
    path("user_dashboard/", views.user_dashboard, name='user_dashboard'),
    path("signup/", views.signup, name='signup'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path("newpassword/", views.newpassword, name='newpassword'),
    path("password_reset/", views.password_reset, name='password_reset'),
    path("password_reset_confirm/<uidb64>/<token>", views.password_reset_confirm, name='password_reset_confirm'),
    path("verify/<uidb64>/<token>", views.verify_email, name='verify'),
]
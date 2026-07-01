from django.urls import path
from .views import profile_view, profile_edit, verification_code, settings_view, delete_account, send_otp_view, verify_otp_view

urlpatterns = [
    path('', profile_view),
    path('edit/', profile_edit, name='profile_edit'),
    path('verification_code/', verification_code, name='verification_code'),
    path('settings/', settings_view, name='settings'),
    path('delete_account/', delete_account, name='delete_account'),
    path('send-otp/', send_otp_view, name='send_otp'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
]

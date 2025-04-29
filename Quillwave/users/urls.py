from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    # ✅ OTP for password reset
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),

    path('reset-password/', views.reset_password, name='reset_password'),
    path('add-info/', views.add_info, name='add_info'),
    path('update-profile/', views.update_profile, name='update_profile'),

    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
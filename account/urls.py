from account.views import PatientSignUpView, DoctorSignUpView, ProfileView, login
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'account'

urlpatterns = [
    path('signup/sick/', PatientSignUpView.as_view(), name='signup-sick'),
    path('signup/doctor/', DoctorSignUpView.as_view(), name='signup-doctor'),
    path('profile/', ProfileView.as_view(), name='profile')
]
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.contrib import messages
from django.conf import settings

from account.models import User, ProfileDoctor, ProfileSick
from account.forms import SickSignUpForms, DoctorSignUpForms
from account.tokens import account_activation_token


def send_email_action(user, request):
        current_site = get_current_site(request)  
        mail_subject = 'لینک فعال سازی'
        message = render_to_string('registration/activate_email.html', {  
            'user': user,  
            'domain': current_site.domain,  
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
            'token':account_activation_token.make_token(user),  
        })
        email = EmailMessage(subject=mail_subject, body=message, from_email= settings.EMAIL_FROM_USER, to=[user.email])
        email.send()

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # if not user.is_email_verify:
            # messages.add_message(request, messages.ERROR, '.ایمیل شما تایید نشده لطفا ایمیل خود را چک کنید')
        if user is not None:
            auth_login(request, user)
            return redirect('account:profile')
        else:
            return redirect('account:login')
    else:
        return redirect('account:login')

class PatientSignUpView(CreateView):
    model = User
    form_class = SickSignUpForms
    template_name = 'registration/signup_sick.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 1
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        send_email_action(user, self.request)
        return HttpResponse('لطفا ایمیل خود را چک کنید ایمیلی حاوی لینک فعال سازی حساب برای شما ارسال شده است .')
        # current_site = get_current_site(self.request)  
        # mail_subject = 'Activation link has been sent to your email id'  
        # message = render_to_string('registration/activate_email.html', {  
        #     'user': user,  
        #     'domain': current_site.domain,  
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
        #     'token':account_activation_token.make_token(user),  
        # })  
        # to_email = form.cleaned_data.get('email')  
        # email = EmailMessage(  
        #             mail_subject, message, to=[to_email]  
        # )  
        # email.send()

class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForms
    template_name = 'registration/signup_doctor.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 2
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save(commit=False)
        return redirect('account:login')

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'registration/profile.html'
    context_object_name = 'sicks'
    
    def get_queryset(self):
        if self.request.user.is_sick == True:
            return ProfileSick.objects.get(user__id=self.request.user.id)
        if self.request.user.is_doctor == True:
            return ProfileDoctor.objects.get(user__id=self.request.user.id)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verify = True
        user.save()
        # return redirect('home')
        return HttpResponse('ایمیل شما با موفقیت فعال شد')
    else:
        return HttpResponse('لینک شما منقضی شده یا نامعتبر است لطفا <a href="/signup/sick">دوباره امتحان کنید.</a>')
from cProfile import label
from dataclasses import fields
from enum import unique
from random import choices
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from account.models import User, ProfileSick, ProfileDoctor, Specialties
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText, PrependedText
from crispy_forms.layout import Layout, ButtonHolder, Submit
from crispy_forms.layout import Field


class SickSignUpForms(UserCreationForm):
    choice_province = (
        ('azarbayejan_sh','آذربایجان شرقی'),('azarbayejan_qh','آذربایجان غربی'),
        ('ardabil','اردبیل'),('esfehan','اصفهان'),
        ('alborz','البرز'),('elam','ایلام'),
        ('bohsher','بوشهر'),('tehran','تهران'),
        ('charmahalbakhtiary','چهار محال و بختیاری'),('khorasan_j','خرسان جنوبی'),
        ('khorasan_r','خراسان رضوی'),('khorasan_sh','خراسان شمالی'),
        ('khozestan','خوزستان'),('zanjan','زنجان'),
        ('semnan','سمنان'),('sistanbalochestan','سیستان و بلوچستان'),
        ('fars','فارس'),('qhazvin','قزوین'),
        ('qhom','قم'),('kordestan','کردستان'),
        ('kerman','کرمان'),('kermanshah','کرمانشاه'),
        ('kohgiloboerahmad','کهگیلویه و بویراحمد'),('golestan','گلستان'),
        ('gilan','گیلان'),('lorestan','لرستان'),
        ('mazandaran','مازندران'),('markazi','مرکزی'),
        ('hormozgan','هرمزگان'),('hamedan','همدان'),
        ('yazd','یزد')
    )
    
    first_name = forms.CharField(max_length=255, required=True, label='نام')
    last_name = forms.CharField(max_length=255, required=True, label='نام خانوادگی')
    national_code = forms.CharField(max_length=10, required=True, label='کد ملی')
    birth_certificate_code = forms.CharField(max_length=10, label='شماره شناسنامه')
    father_name = forms.CharField(max_length=255, label='نام پدر')
    province_of_residence = forms.ChoiceField(choices=choice_province, label='استان محل زندگی')
    phone_number = forms.CharField(max_length=11, label='شماره موبایل')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    @transaction.atomic
    def save(self, commit):
        user = super().save(commit=False)
        user.is_sick = True
        user.save()
        ProfileSick.objects.create(
                user=user,
                first_name = self.cleaned_data['first_name'],
                last_name = self.cleaned_data['last_name'],
                national_code = self.cleaned_data['national_code'],
                birth_certificate_code = self.cleaned_data['birth_certificate_code'],
                father_name = self.cleaned_data['father_name'],
                province_of_residence = self.cleaned_data['province_of_residence'],
                phone_number = self.cleaned_data['phone_number'],
        )
        
        return user


class DoctorSignUpForms(UserCreationForm):
    first_name = forms.CharField(max_length=255, label='نام')
    last_name = forms.CharField(max_length=255, label='نام خانواادگی')
    address_office = forms.CharField(widget=forms.Textarea, label='آدرس مطب')
    expertise = forms.ModelChoiceField(queryset=Specialties.objects.all(), label='تخصص')
    telphone_number_office = forms.CharField(max_length=11, label='تلفن مطب')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    @transaction.atomic
    def save(self, commit):
        user = super().save(commit=False)
        user.is_doctor = True
        user.user_type = 2
        user.save()
        ProfileDoctor.objects.create(
                user = user,
                first_name = self.cleaned_data['first_name'],
                last_name = self.cleaned_data['last_name'],
                address_office = self.cleaned_data['address_office'],
                expertise = self.cleaned_data['expertise'],
                telphone_number_office = self.cleaned_data['telphone_number_office'],
                image_profile = self.cleaned_data['image_profile'],
        )
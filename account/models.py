from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Specialties(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='childern', verbose_name='تخصص')
    title = models.CharField(max_length=255, verbose_name='عنوان تخصص')
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name='لینک کوتاه')

    def __str__(self):
        return self.title

class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'sick'),
      (2, 'doctor'),
      (3, 'secretary'),
      (4, 'admin'),
    )
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_email_verify = models.BooleanField(default=False) 
    is_sick = models.BooleanField(default=False, blank=True)
    is_doctor = models.BooleanField(default=False, blank=True)
    is_secretary = models.BooleanField(default=False, blank=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)


class ProfileSick(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')
    birth_certificate_code =  models.CharField(max_length=10, unique=True, verbose_name='شماره شناسنامه')
    father_name = models.CharField(max_length=255, verbose_name='نام پدر')
    province_of_residence = models.CharField(max_length=18, choices=choice_province, verbose_name='استان محل زندگی')
    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    image_profile = models.ImageField(upload_to='image profile sick', verbose_name='عکس پروفایل')
    is_sick = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name


class ProfileDoctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    first_name = models.CharField(max_length=255, verbose_name='نام')
    last_name = models.CharField(max_length=255, verbose_name='نام خانوادگی')
    address_office = models.TextField(verbose_name='آدرس مطب')
    expertise = models.ForeignKey(Specialties, on_delete=models.PROTECT, verbose_name='تخصص')
    telphone_number_office = models.CharField(max_length=11, verbose_name='تلفن مطب')
    image_profile = models.ImageField(upload_to='image profile doctor', verbose_name='عکس پروفایل')
    is_doctor = models.BooleanField(default=True)

    def __str__(self):
        return self.first_name
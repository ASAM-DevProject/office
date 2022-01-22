from turtle import mode
from django.db import models
from account.views import User, ProfileSick, ProfileDoctor


class Visit(models.Model):
    sick = models.ForeignKey(ProfileSick, on_delete=models.PROTECT)
    doctor = models.ForeignKey(ProfileDoctor, on_delete=models.PROTECT)
    
    
    
from pyexpat import model
from django.shortcuts import render
from django.views.generic import ListView

from visit.models import Visit

# Create your views here.

# class VisitList(ListView):
#     model = Visit
#     template_name = 'visit/visit.html'
#     context_object_name = 'visits'
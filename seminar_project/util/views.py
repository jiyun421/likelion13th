from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse  


def health(request):               
    return HttpResponse(status = 200, content = "seminar server ok!")

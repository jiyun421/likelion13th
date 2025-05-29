from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse  
from rest_framework.decorators import api_view

@api_view(['GET'])
def health(request):               
    return HttpResponse(status = 200, content = "seminar server ok!")

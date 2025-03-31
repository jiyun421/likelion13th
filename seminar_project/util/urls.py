from django.contrib import admin
from django.urls import path  

from . import views  # 현재 디렉토리의 util/views.py 파일에서 뷰 함수들을 import 합니다.

urlpatterns = [
    path('health/', views.health),  # util 앱의 기본 URL ('/') 은 views.py의 health 함수와 연결합니다.
    # 즉, util/urls.py의 기본 경로에 대한 요청은 views.py 파일의 health 함수로 처리됩니다.
]

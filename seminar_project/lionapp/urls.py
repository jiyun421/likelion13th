from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('create/',views.create_post),
    path('get/<int:pk>/',views.get_post), 
    path('all/',views.get_posts_all),
    path('update/<int:pk>/',views.update_post), 
    path('delete/<int:pk>/',views.delete_post),
    path('comments/<int:post_id>',views.get_comment),
    path('v2/post',views.create_post_v2), # FBV
    path('v2/post/<int:pk>',views.PostApiView.as_view()),
    path('v2/post/all',views.PostApiView.as_view()) # 전체조회
]
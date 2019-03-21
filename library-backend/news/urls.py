from django.urls import path
from . import views


urlpatterns = [
     path('get/news/', views.get_news),
     path('get/detail/', views.get_news_detail),
     path('get/summary/', views.get_summary),
     path('get/service/', views.service_summary),
     path('get/summary/', views.service_summary),

     path('post/file/', views.post_file)
]

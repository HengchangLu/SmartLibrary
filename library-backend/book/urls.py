from django.urls import path
from . import views


urlpatterns = [
     # path('search/', views.book_info),
     path('get/newbook/', views.get_book_list),
     path('renew/', views.renew_book),
     path('search/', views.search_book),
     path('detail/', views.book_detail),
     path('borrowed/', views.borrowed_book),
]

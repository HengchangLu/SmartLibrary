from django.urls import path
from . import views
urlpatterns = [
    path('gitpull/', views.pull),
]
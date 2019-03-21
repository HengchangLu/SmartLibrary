from django.urls import path
from . import views

urlpatterns = (
     path('login/appoint/seat/', views.login_lib_or_appoint),
     path('post/feedback/', views.get_feedback_msg),
     path('test/mail/', views.test_send_email),
)

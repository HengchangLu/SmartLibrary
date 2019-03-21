from django.urls import path
from . import views
# from django.views.static import serve
# from django.conf.urls import url
# from django.conf import settings
# from django.conf.urls.static import static
urlpatterns = (
    path('seat/region/', views.get_region),
    path('get/seat/', views.get_seat),
    path('reserve/seat/', views.reserve_seat),
)

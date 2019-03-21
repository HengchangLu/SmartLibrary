from django.http import HttpResponse
import json
from django.shortcuts import render
from .models import UserLocation
# Create your views here.


def save_position(request):
    """

    """
    latitude = request.GET['latitude']
    longitude = request.GET['longitude']
    location = UserLocation()
    location.latitude = latitude
    location.longitude = longitude
    location.save()
    # return HttpResponse(json.dumps(response, ensure_ascii=False))

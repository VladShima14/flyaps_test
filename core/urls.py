from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    path('api/calendar', views.CalendarApi.as_view(), name='Calendar'),
]

from django.shortcuts import render

from rest_framework import generics
from rest_framework.generics import ListAPIView

from .models import Agreement
from .api.serializers import AgreementSerializer
# Create your views here.


class CalendarApi(generics.ListAPIView):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer

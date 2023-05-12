from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
import django_filters

from .serializers import *
from .models import *
from rest_framework.response import Response
from django.shortcuts import render


class SchoolViewset(viewsets.ModelViewSet):
    queryset = School.objects.all().filter(is_active=True)
    serializer_class = SchoolSerializer

    def destroy(self, request, pk, format=None):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SClassViewset(viewsets.ModelViewSet):
    queryset = SClass.objects.all()
    serializer_class = SClassSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["grade", "school_id"]


class StudentViewest(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

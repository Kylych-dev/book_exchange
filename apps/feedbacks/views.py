from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers

class RatingViewSet(ModelViewSet):
    serializer_class = serializers.RatingSerializer
    permission_classes = [IsAuthenticated]
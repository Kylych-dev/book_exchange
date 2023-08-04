from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]
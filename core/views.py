from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework import (
    generics
)
from rest_framework.response import Response

from . import models
from rest_framework import serializers

from django_filters import rest_framework as filters
import django_filters

class AlbumFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    artist__first_name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = models.Album 
        fields = ["name", "num_stars", "artist__first_name"]

class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Musician
        fields = "__all__"

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album


class MusicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Musician
        fields = "__all__"

class AlbumSerializer(serializers.ModelSerializer):
    artist = MusicianSerializer()
    class Meta:
        model = models.Album
        fields = ["id", "name", "num_stars", "artist"]


class API(generics.ListAPIView):
    queryset = models.Album.objects.select_related("artist")
    serializer_class = AlbumSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    #filterset_fields = ('name', "num_stars", "artist__first_name")
    filterset_class = AlbumFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = self.queryset.filter(id=1)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
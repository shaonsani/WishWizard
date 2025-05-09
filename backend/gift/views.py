from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Gift, FavouritePerson, GiftEvent
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q, F
from .serializers import GiftSerializer, FavouritePersonSerializer, GiftEventSerializer

class GiftListAPIView(APIView):
    permission_classes = []

    def get(self, request):
        gifts = Gift.objects.all()
        serializer = GiftSerializer(gifts, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
    
        data = request.data
        serializer = GiftSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.urls import path
from django.conf import settings
from .views import GiftListAPIView

urlpatterns = [
   path("gifts/", GiftListAPIView.as_view(), name="gift-list"),
]

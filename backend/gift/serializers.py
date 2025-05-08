from rest_framework import serializers
from .models import FavouritePerson, Gift, GiftEvent
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = "__all__"


class GiftEventSerializer(serializers.ModelSerializer):
    gift = GiftSerializer(read_only=True)
    class Meta:
        model = GiftEvent
        fields = ["id", "gift", "sent_at", "created_at", "updated_at"]


class FavouritePersonSerializer(serializers.ModelSerializer):
    next_birthday = serializers.SerializerMethodField()
    gift_events = GiftEventSerializer(many=True, read_only=True)
    class Meta:
        model = FavouritePerson
        fields = [
            "id",
            "name",
            "birth_date",
            "preference_vector",
            "created_at",
            "updated_at",
            "next_birthday",
            "gift_events",
        ]

    def get_next_birthday(self, obj: FavouritePerson):
        """
        Calculate the next birthday of the person.
        """
        today = timezone.localdate()
        next_birthday = obj.birth_date.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return next_birthday
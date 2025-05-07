from django.conf import settings
from django.db import models
from datetime import date


class FavouritePerson(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourite_persons",
        help_text="The user who added this person to their favourites",
    )
    name = models.CharField(max_length=255, help_text="The name of the person")
    email = models.EmailField(
        max_length=255, help_text="The email address of the person"
    )
    phone = models.CharField(max_length=20, help_text="The phone number of the person")
    birth_date = models.DateField(help_text="Birthday in YYYY‑MM‑DD format")
    preference_vector = models.JSONField(
        help_text="A JSON field to store the preference vector for the person"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the person was added to favourites",
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="The date and time when the person was last updated"
    )

    class Meta:
        verbose_name = "Favourite Person"
        verbose_name_plural = "Favourite Persons"
        ordering = ["-created_at"]
        unique_together = (("name", "email"),)

    def age(self, today: date | None = None) -> int:
        """
        Calculate the age of the person based on their birth date.
        """

        today = today or date.today()
        age = (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
        return age

    def __str__(self) -> str:
        return f"{self.name} ({self.birth_date:%d %b})"

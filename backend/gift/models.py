from django.conf import settings
from django.db import models
from datetime import date
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The date and time when the object was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The date and time when the object was last modified."),
    )

    class Meta:
        abstract = True
        ordering = ("-created_at",)
        

class FavouritePerson(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourite_persons",
        help_text=_("The user who added this person to their favourites"),
    )
    name = models.CharField(max_length=255, help_text=_("The name of the person"))
    email = models.EmailField(
        max_length=255, help_text=_("The email address of the person")
    )
    phone = models.CharField(max_length=20, help_text=_("The phone number of the person"))
    birth_date = models.DateField(help_text=_("Birthday in YYYY‑MM‑DD format"))
    preference_vector = models.JSONField(
        help_text=_("A JSON field to store the preference vector for the person")
    )

    class Meta(TimeStampedModel.Meta):
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
    

class Gift(TimeStampedModel):
    """
    A product that can potentially be recommended.

    """

    title = models.CharField(
        max_length=255,
        help_text=_("Product title / name as shown on the merchant site."),
    )
    description = models.TextField(
        blank=True,
        help_text=_("Plain‑text description scraped from the listing."),
    )
    url = models.URLField(
        unique=True,
        help_text=_("Canonical URL to the merchant page."),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Price in the merchant's default currency"),
    )
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text=_("List of categorical tags, e.g. ['chocolates', 'toy', 'kids']."),
    )
    embedding_vector = models.JSONField(
        default=list,
        blank=True,
        help_text=_("Dense text+image embedding for semantic similarity."),
    )

    class Meta(TimeStampedModel.Meta):
        indexes = [
            models.Index(fields=["title"], name="gift_title_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.price} {settings.DEFAULT_CURRENCY})"


class GiftEvent(TimeStampedModel):
    """
    Audit table recording each gift that was actually sent.

    """

    favourite_person = models.ForeignKey(
        FavouritePerson,
        on_delete=models.CASCADE,
        related_name="gift_events",
        help_text=_("Recipient of the gift."),
    )
    gift = models.ForeignKey(
        Gift,
        on_delete=models.CASCADE,
        help_text=_("Gift that was purchased / given."),
    )
    sent_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Timestamp when the gift was marked as sent."),
    )

    class Meta(TimeStampedModel.Meta):
        ordering = ("-sent_at",)
        get_latest_by = "sent_at"
        unique_together = ("favourite_person", "gift")

    def __str__(self) -> str:
        return (
            f"{self.gift.title} → {self.favourite_person.name} "
            f"on {self.sent_at:%Y‑%m‑%d}"
        )
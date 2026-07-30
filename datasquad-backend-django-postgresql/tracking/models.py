import uuid

from django.db import models


class Visit(models.Model):
    """Une visite = un chargement de page sur le site Data Squad."""

    DEVICE_CHOICES = [
        ("desktop", "Ordinateur"),
        ("mobile", "Mobile"),
        ("tablet", "Tablette"),
        ("bot", "Robot"),
        ("other", "Autre"),
    ]

    visitor_id = models.UUIDField(
        default=uuid.uuid4,
        db_index=True,
        help_text="Identifiant anonyme stocké dans un cookie, stable entre les visites.",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    path = models.CharField(max_length=500, help_text="Page visitée, ex: /en/projets.html")
    referrer = models.CharField(max_length=500, blank=True, default="")
    lang = models.CharField(max_length=10, blank=True, default="", help_text="fr / en / ar déduit de l'URL")

    user_agent = models.TextField(blank=True, default="")
    browser = models.CharField(max_length=50, blank=True, default="")
    os = models.CharField(max_length=50, blank=True, default="")
    device_type = models.CharField(max_length=10, choices=DEVICE_CHOICES, default="other")

    country = models.CharField(max_length=100, blank=True, default="")
    is_new_visitor = models.BooleanField(default=False, help_text="Première visite jamais enregistrée pour ce visitor_id")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["visitor_id"]),
        ]

    def __str__(self):
        return f"{self.path} · {self.created_at:%Y-%m-%d %H:%M}"

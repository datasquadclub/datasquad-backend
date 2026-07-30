from django.db import models


class TeamMember(models.Model):
    name = models.CharField("Nom complet", max_length=150)
    initials = models.CharField(
        "Initiales (avatar)", max_length=4, blank=True,
        help_text="Ex: CB. Laissez vide pour les déduire automatiquement du nom.",
    )
    role = models.CharField("Rôle", max_length=200)
    mission = models.TextField("Mission / description")
    photo = models.ImageField("Photo", upload_to="equipe/", blank=True, null=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_published = models.BooleanField("Publié sur le site", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Équipe"

    def __str__(self):
        return self.name


class NewsPost(models.Model):
    title = models.CharField("Titre", max_length=250)
    date_label = models.CharField(
        "Date affichée", max_length=50,
        help_text="Texte libre affiché tel quel, ex: Juillet 2026",
    )
    body = models.TextField("Texte")
    photo = models.ImageField("Photo", upload_to="actus/", blank=True, null=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0, help_text="Plus petit = affiché en premier")
    is_published = models.BooleanField("Publié sur le site", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __str__(self):
        return self.title

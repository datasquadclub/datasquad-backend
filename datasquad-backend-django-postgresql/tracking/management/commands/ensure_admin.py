import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Crée (ou met à jour le mot de passe d') un compte super-admin à partir
    des variables d'environnement DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD.

    But: permettre de créer le premier compte admin sur un hébergeur sans
    accès terminal (Railway, Render...), juste en remplissant des variables
    d'environnement dans leur interface web, puis en redéployant. Commande
    idempotente : peut être appelée à chaque démarrage sans risque.
    """

    help = "Crée/actualise un super-admin depuis les variables d'environnement (sans terminal)."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write("DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD non définis, étape ignorée.")
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username, defaults={"email": email})
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(("Compte admin créé: " if created else "Compte admin mis à jour: ") + username))

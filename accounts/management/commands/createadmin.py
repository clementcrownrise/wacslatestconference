import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create the initial superuser if one does not exist."

    def handle(self, *args, **kwargs):
        User = get_user_model()

        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        first_name = os.getenv("DJANGO_SUPERUSER_FIRST_NAME", "Admin")
        last_name = os.getenv("DJANGO_SUPERUSER_LAST_NAME", "User")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not email or not username or not password:
            self.stdout.write(
                self.style.ERROR(
                    "Missing one or more required environment variables:\n"
                    "DJANGO_SUPERUSER_EMAIL\n"
                    "DJANGO_SUPERUSER_USERNAME\n"
                    "DJANGO_SUPERUSER_PASSWORD"
                )
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Superuser '{email}' already exists."
                )
            )
            return

        User.objects.create_superuser(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Superuser '{email}' created successfully."
            )
        )
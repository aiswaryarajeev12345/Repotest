import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import UserProfile


class Command(BaseCommand):
    help = "Create or update the emergency coordinator account"

    def handle(self, *args, **options):
        username = "coordinator"
        password = os.environ.get("COORDINATOR_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.ERROR(
                    "COORDINATOR_PASSWORD environment variable is not set."
                )
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": "coordinator@example.com"}
        )

        user.set_password(password)
        user.save()

        profile, profile_created = UserProfile.objects.get_or_create(
            user=user
        )
        profile.role = "COORDINATOR"
        profile.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS("Coordinator account created successfully.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Coordinator account updated successfully.")
            )
from django.core.management.base import BaseCommand
from django.utils import timezone

from panel.models import OTP

from datetime import timedelta

class Command(BaseCommand):
    help = 'remove all expire otp codes'

    def handle(self, *args, **options):
        OTP.objects.filter(created__lt=timezone.now()-timedelta(minutes=3)).delete()
        self.stdout.write('expire otp code deleted successfully')
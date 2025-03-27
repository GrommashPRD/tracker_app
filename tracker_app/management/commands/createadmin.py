import os
import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_NAME', default='root')
        email = os.environ.get('ADMIN_EMAIL', default='admin@example.com')
        password = os.environ.get('ADMIN_PASS', default='root')
        try:
            if not User.objects.filter(username=username).exists() and not User.objects.filter(
                    is_superuser=True).exists():
                logger.info('Admin user not found, creating one')

                User.objects.create_superuser(username, email, password)
                logger.info(
                    'A superuser (%s) was created with email (%s) and password (%s);',
                    username,
                    email,
                    password
                )

            else:
                logger.info('Аdmin user found by. Skipping super user creation')
        except Exception as err:
            logger.error('There was an error: %s', err)
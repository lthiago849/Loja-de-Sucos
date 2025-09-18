import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'App.settings')
django.setup()

from django.contrib.auth.models import User

user, created = User.objects.get_or_create(
    username='sol',
    defaults={
        'email': 'sol@test.com', 
        'is_staff': True,
        'is_superuser': True
    }
)
user.set_password('Solbarros26031605?')
user.save()
print('Usuario sol criado!')
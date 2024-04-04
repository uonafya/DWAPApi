from django.contrib.auth.models import Group
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import RoleScreens
User=get_user_model()

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        roles = ['admin']
        for role in roles:
            role, created = Group.objects.get_or_create(name=role)
            screens,created=RoleScreens.objects.get_or_create(role_id=role)
        if User.objects.filter(username='admin').first() == None:
            admin, created = User.objects.get_or_create(
                email='admin@bengohub.co.ke',
                defaults={
                    "username": 'admin',
                    "password": '@Admin123',
                    "first_name": 'bengo',
                    "last_name": 'hub',
                    "phone": '+254743793901',
                    "is_active": True,
                    "is_staff": True,
                    "is_superuser": True
                }
            )
            # print(admin.password)
            admin.groups.add(Group.objects.get(name='admin'))
            admin.save()
        response = self.get_response(request)
        return response
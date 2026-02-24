#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOFT806_WK3_Chatroom.settings')
django.setup()

from chat.models import UserProfile

# Create admin user
try:
    admin = UserProfile.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print(f"Admin user created: {admin.username}")
    print("Login credentials:")
    print("Username: admin")
    print("Password: admin123")
except Exception as e:
    print(f"Error creating admin: {e}")

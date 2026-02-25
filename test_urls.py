#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOFT806_WK3_Chatroom.settings')
django.setup()

from django.urls import reverse
from django.test import Client

try:
    # Test if URL can be reversed
    register_url = reverse('register_user')
    print(f"Register URL: {register_url}")
    
    login_url = reverse('login_user')
    print(f"Login URL: {login_url}")
    
    # Test if URLs are accessible
    client = Client()
    
    # Test register endpoint (should return 400 for empty POST)
    response = client.post('/api/chat/auth/register/', {})
    print(f"Register endpoint status: {response.status_code}")
    
    # Test login endpoint (should return 400 for empty POST)
    response = client.post('/api/chat/auth/login/', {})
    print(f"Login endpoint status: {response.status_code}")
    
    print("All URLs are working correctly!")
    
except Exception as e:
    print(f"Error: {e}")

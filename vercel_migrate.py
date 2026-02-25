#!/usr/bin/env python
import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SOFT806_WK3_Chatroom.settings')
django.setup()

def run_migrations():
    """Run Django migrations on Vercel deployment"""
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("Migrations completed successfully")
    except Exception as e:
        print(f"Migration error: {e}")
        raise

if __name__ == '__main__':
    run_migrations()

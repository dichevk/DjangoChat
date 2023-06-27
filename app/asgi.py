import os 
from django.core.asgi import get_asgi_application

''' This is the asynchronous gateway interface configuration for the python django application
    The application variable exposes the ASGI callable and the settings are configured within the settings.py under DJANGO_SETTINGS_MODULE
'''

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

application = get_asgi_application

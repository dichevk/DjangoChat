import os 
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import URLResolver, ProtocolTypeRouter
from app import routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': asgi_application,
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLResolver(routing.websocket_urlpatterns)))

})


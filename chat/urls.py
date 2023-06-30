from django.contrib import admin
from django.urls import path, include

urlpatterns:list = [
    
    path('', include('core.urls')),
    path('', include('chat.urls')),
    path('', include('account.urls'))
]

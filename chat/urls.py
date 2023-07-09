from django.urls import path, include

urlpatterns:list = [
    
    path('', include('core.urls')),
    path('', include('app.urls')),
    path('', include('account.urls'))
]

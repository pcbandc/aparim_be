from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/counterparties/', include('counterparties.urls')),
    path('api/v1/auth/', include('auth.urls')),
    path('api/v1/stock/', include('stock.urls')),
]

"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from MediaApp.views import MediaViewSet
from PlayerApp.views import PlayerViewSet

api_routers = routers.DefaultRouter()
api_routers.register('api/media', MediaViewSet, basename="media")
api_routers.register('api/player', PlayerViewSet, basename="player")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(api_routers.urls)),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('media/', include('MediaApp.urls')),  # Include the MediaApp app's URL patterns
    path('player/', include('PlayerApp.urls')),  # Include the PlayerApp app's URL patterns
]

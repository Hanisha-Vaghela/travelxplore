"""
URL configuration for mywebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
"""
URL configuration for mywebsite project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Traveler CRUD
    path('travelers/', views.traveler_list, name='traveler_list'),
    path('travelers/add/', views.traveler_create, name='traveler_create'),
    path('travelers/edit/<int:id>/', views.traveler_update, name='traveler_update'),
    path('travelers/delete/<int:id>/', views.traveler_delete, name='traveler_delete'),
    
    # Contact Messages
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:id>/', views.message_detail, name='message_detail'),
    path('messages/delete/<int:id>/', views.message_delete, name='message_delete'),
    
    # Destinations (Admin Only - except detail view)
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/add/', views.destination_create, name='destination_create'),
    path('destinations/edit/<int:id>/', views.destination_update, name='destination_update'),
    path('destinations/delete/<int:id>/', views.destination_delete, name='destination_delete'),
    path('destinations/<int:id>/', views.destination_detail, name='destination_detail'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
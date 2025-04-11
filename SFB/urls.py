"""
URL configuration for SFB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.urls import path
from syndicat.views import add_subscriber, edit_subscriber, delete_subscriber_ajax, call_webservice, \
    check_siret_ajax, home, login_view, register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_view, name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', register, name='register'),
    path('accueil', home, name='home'),
    path('ajouter-adherent', add_subscriber, name='add_subscriber'),
    path('editer-adherent/<int:subscriber_id>', edit_subscriber, name='edit_subscriber'),
    path('ajax/supprimer-adherent',delete_subscriber_ajax, name='delete_subscriber_ajax'),
    path('webservice', call_webservice, name='call_webservice'),
    path('check-siret/ajax/', check_siret_ajax, name='check_siret_ajax'),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

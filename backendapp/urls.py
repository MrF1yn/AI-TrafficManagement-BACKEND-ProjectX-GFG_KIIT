"""
URL configuration for aitrafficmanagementsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
                  path('home', views.home, name="home"),
                  path('errorpage', views.errorpage, name="errorpage"),
                  path('signin', views.signin, name="signin"),
                  path('register', views.signup, name="signup"),
                  path('signout', views.signout, name="signout"),
                  path('user', views.user_func, name="user"),
                  path('results', views.results_func, name="results"),
                  path('map', views.map_func, name="map"),
                  # path('upload', views.upload_video, name='upload_video'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

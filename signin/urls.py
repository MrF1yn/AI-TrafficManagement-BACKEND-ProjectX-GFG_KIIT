from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('errorpage', views.errorpage, name="errorpage"),
    path('', views.signin, name="signin"),
    path('register', views.signup, name="signup"),
    path('signout', views.signout, name="signout"),
    path('user', views.user_func, name="user"),
    path('results', views.results_func, name="results"),
    path('map', views.map_func, name="map"),
    # path('upload', views.upload_video, name='upload_video'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
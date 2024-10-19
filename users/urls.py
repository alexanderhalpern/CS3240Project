from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('main/', views.main, name="main"),
    path('logout/', views.logout_view, name="logout"),
    path('update_profile', views.update_profile, name = 'update_profile'),
]

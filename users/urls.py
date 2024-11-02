from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('', views.home, name="home"),
    path('main/', views.main, name="main"),
    path('logout/', views.logout_view, name="logout"),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('<int:id>/', views.projectView, name='specific-project'),
    path('<int:id>/files/', views.filesView, name="project-files"),
    path('event/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('event/create', views.create_event, name='create_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
]

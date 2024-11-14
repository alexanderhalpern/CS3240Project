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
    path('event/<int:event_id>/delete/',
         views.delete_event, name='delete_event'),
    path('<int:id>/members/', views.membersView, name="view-members"),
    path('projects/<int:project_id>/modal-content/',
         views.project_modal, name='project-modal'),
    path('projects/<int:project_id>/delete/',
         views.delete_project, name='delete-project'),
    path('projects/<int:project_id>/members/add/',
         views.add_member, name='add-member'),
    path('projects/<int:project_id>/members/<int:user_id>/remove/',
         views.remove_member, name='remove-member'),
    path('projects/<int:project_id>/join/',
         views.join_project, name='join-project'),

]

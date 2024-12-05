from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('', views.home, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('cio/<slug:slug>/calendar/', views.calendar_view, name='cio-calendar'),
    path('<int:id>/', views.projectView, name='specific-project'),
    path('<int:id>/files/', views.filesView, name="project-files"),
    path('event/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('event/create/<slug:slug>/', views.create_event, name='create_event'),
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
         path('projects/<int:project_id>/leave/',
         views.leave_project, name='leave-project'),
    path('cio/<slug:slug>/', views.cio_detail, name='cio-detail'),
    path('cio/<slug:slug>/join/', views.join_cio, name='join-cio'),
    path('cio/<slug:slug>/leave/', views.leave_cio, name='leave-cio'),
    path('cio/<slug:slug>/create-announcement/', views.create_announcement, name='create-announcement'),
    path('cio/<slug:slug>/announcements/<int:announcement_id>/delete/', views.delete_announcement, name='delete-announcement'),
    path('cio/<slug:slug>/dashboard/', views.cio_dashboard, name="cio-dashboard"),
    path('cio/<slug:slug>/calendar/', views.calendar_view, name='cio-calendar'),
    path('cio/<slug:slug>/members/add/',
         views.add_cio_member, name='add-cio-member'),
    path('event/<int:event_id>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('event/<int:event_id>/rsvps/', views.view_rsvps, name='view_rsvps'),
    path('cio/<slug:slug>/admins/add/',
         views.add_cio_admin, name='add-cio-admin'),
    path('cio/<slug:slug>/members/', views.cio_members, name='cio-members'),
    path('cio/<slug:slug>/admin-files/', views.admin_files_view, name='admin-files'),

    path('add-cio/', views.add_cio, name='add-cio'),
    path('guest-view/', views.continue_as_guest, name="guest-view"),
    path('mailbox/', views.mailbox, name='mailbox'),
    path('notifications/<int:notification_id>/mark-as-read/', views.mark_as_read, name='mark_as_read'),
    path('mark-all-as-read/', views.mark_all_as_read, name='mark_all_as_read'),
    path('contact-support/', views.contact_support, name='contact_support'),
    path('support-messages/', views.support_messages, name='support_messages'),
    path('cio/<slug:slug>/announcements/', views.announcements_page, name='cio-announcements'),
    path('file/<int:file_id>/delete/', views.delete_file, name='delete-file'),
    path('project/<int:project_id>/request-to-join/', views.request_to_join_project, name='request-to-join-project'),
    path('project/<int:project_id>/handle-join-request/<int:user_id>/<str:action>/', 
         views.handle_join_request, name='handle-join-request'),
    path('project/<int:id>/members/', views.membersView, name='view-members'),
    path('view-projects/', views.view_projects, name='view-projects'),

]

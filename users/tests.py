from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from users.models import (
    CIO, Profile, Project, File, AdminFile, Event, RSVP,
    Notification, Announcement, SupportMessage
)
from datetime import date, time
from django.core.files.uploadedfile import SimpleUploadedFile

class CIOModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cio = CIO.objects.create(name="Test CIO", description="Test CIO Description")

    def test_cio_slug_creation(self):
        self.assertEqual(self.cio.slug, "test-cio")

    def test_cio_admins_and_members(self):
        self.cio.admins.add(self.user)
        self.cio.members.add(self.user)
        self.assertIn(self.user, self.cio.admins.all())
        self.assertIn(self.user, self.cio.members.all())

    def test_cio_absolute_url(self):
        self.assertEqual(self.cio.get_absolute_url(), f"/cio/{self.cio.slug}/dashboard/")


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.profile = Profile.objects.create(user=self.user, bio="Test Bio")

    def test_profile_str_representation(self):
        self.assertEqual(str(self.profile), "testuser's profile")


class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cio = CIO.objects.create(name="Test CIO", description="Test Description")
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Project Description",
            created_by=self.user,
            cio=self.cio
        )

    def test_project_str_representation(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_project_members(self):
        self.project.members.add(self.user)
        self.assertIn(self.user, self.project.members.all())


class FileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cio = CIO.objects.create(name="Test CIO", description="Test Description")
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Project Description",
            created_by=self.user,
            cio=self.cio
        )
        self.file = File.objects.create(
            project=self.project,
            file=SimpleUploadedFile("test_file.txt", b"content of the file"),
            uploaded_by=self.user
        )

    def test_file_save_metadata(self):
        self.assertEqual(self.file.file_name, "test_file.txt")
        self.assertEqual(self.file.file_type, "txt")
        self.assertEqual(self.file.file_size, len(b"content of the file"))


class AdminFileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cio = CIO.objects.create(name="Test CIO", description="Test Description")
        self.admin_file = AdminFile.objects.create(
            file="admin_file.txt",
            uploaded_by=self.user,
            club=self.cio
        )

    def test_admin_file_str_representation(self):
        self.assertEqual(str(self.admin_file), "admin_file.txt")


class EventModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cio = CIO.objects.create(name="Test CIO", description="Test Description")
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Event Description",
            date=date.today(),
            time=time(12, 0),
            created_by=self.user,
            cio=self.cio
        )

    def test_event_str_representation(self):
        self.assertEqual(str(self.event), f"Test Event on {date.today()}")


class RSVPModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cio = CIO.objects.create(name="Test CIO", description="Test Description")
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Event Description",
            date=date.today(),
            time=time(12, 0),
            created_by=self.user,
            cio=self.cio
        )
        self.rsvp = RSVP.objects.create(event=self.event, user=self.user)

    def test_rsvp_str_representation(self):
        self.assertEqual(str(self.rsvp), f"testuser RSVP for Test Event")


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.notification = Notification.objects.create(
            user=self.user,
            content="Test Notification"
        )

    def test_notification_str_representation(self):
        self.assertEqual(str(self.notification), "Notification for testuser: Test Notification")


class AnnouncementModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cio = CIO.objects.create(name="Test CIO", description="Test Description")
        self.announcement = Announcement.objects.create(
            cio=self.cio,
            created_by=self.user,
            content="Test Announcement"
        )

    def test_announcement_str_representation(self):
        self.assertEqual(str(self.announcement), f"Announcement by testuser in Test CIO")


class SupportMessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.support_message = SupportMessage.objects.create(
            user=self.user,
            message="Test Support Message"
        )

    def test_support_message_str_representation(self):
        self.assertEqual(str(self.support_message), f"Message from testuser at {self.support_message.submitted_at}")

class URLTests(TestCase):

    def setUp(self):
        #create dummy user
        self.user = User.objects.create_user(username="testuser", password="password")
        
        #create dummy CIO
        self.cio = CIO.objects.create(name="Test CIO", description="Test description")
        self.cio.admins.add(self.user)
        
        #create dummy project
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Project Description",
            created_by=self.user,
            cio=self.cio
        )
        
        #create dummy event
        self.event = Event.objects.create(
            name="Test Event",
            description="Test Event Description",
            date="2024-12-31",
            time="12:00:00",
            created_by=self.user,
            cio=self.cio
        )

    def test_home_url(self):
        url = reverse("users:home")
        self.assertEqual(resolve(url).view_name, "users:home")

    def test_logout_url(self):
        url = reverse("users:logout")
        self.assertEqual(resolve(url).view_name, "users:logout")

    def test_update_profile_url(self):
        url = reverse("users:update_profile")
        self.assertEqual(resolve(url).view_name, "users:update_profile")

    def test_cio_calendar_url(self):
        url = reverse("users:cio-calendar", kwargs={"slug": self.cio.slug})
        self.assertEqual(resolve(url).view_name, "users:cio-calendar")

    def test_specific_project_url(self):
        url = reverse("users:specific-project", kwargs={"id": self.project.id})
        self.assertEqual(resolve(url).view_name, "users:specific-project")

    def test_project_files_url(self):
        url = reverse("users:project-files", kwargs={"id": self.project.id})
        self.assertEqual(resolve(url).view_name, "users:project-files")

    def test_rsvp_event_url(self):
        url = reverse("users:rsvp_event", kwargs={"event_id": self.event.id})
        self.assertEqual(resolve(url).view_name, "users:rsvp_event")

    def test_create_event_url(self):
        url = reverse("users:create_event", kwargs={"slug": self.cio.slug})
        self.assertEqual(resolve(url).view_name, "users:create_event")

    def test_delete_event_url(self):
        url = reverse("users:delete_event", kwargs={"event_id": self.event.id})
        self.assertEqual(resolve(url).view_name, "users:delete_event")

    def test_view_members_url(self):
        url = reverse("users:view-members", kwargs={"id": self.project.id})
        self.assertEqual(resolve(url).view_name, "users:view-members")

    def test_cio_detail_url(self):
        url = reverse("users:cio-detail", kwargs={"slug": self.cio.slug})
        self.assertEqual(resolve(url).view_name, "users:cio-detail")

    def test_join_cio_url(self):
        url = reverse("users:join-cio", kwargs={"slug": self.cio.slug})
        self.assertEqual(resolve(url).view_name, "users:join-cio")

    def test_leave_cio_url(self):
        url = reverse("users:leave-cio", kwargs={"slug": self.cio.slug})
        self.assertEqual(resolve(url).view_name, "users:leave-cio")

    def test_create_announcement_url(self):
        url = reverse("users:create-announcement", kwargs={"slug": self.cio.slug})
        self.assertEqual(resolve(url).view_name, "users:create-announcement")

    def test_cio_dashboard_url(self):
        url = reverse("users:cio-dashboard", kwargs={"slug": self.cio.slug})
        self.assertEqual(resolve(url).view_name, "users:cio-dashboard")

    def test_announcements_page_url(self):
        url = reverse("users:cio-announcements", kwargs={"slug": self.cio.slug})
        self.assertEqual(resolve(url).view_name, "users:cio-announcements")

    def test_contact_support_url(self):
        url = reverse("users:contact_support")
        self.assertEqual(resolve(url).view_name, "users:contact_support")

    def test_mark_as_read_url(self):
        url = reverse("users:mark_as_read", kwargs={"notification_id": 1})
        self.assertEqual(resolve(url).view_name, "users:mark_as_read")

    def test_mark_all_as_read_url(self):
        url = reverse("users:mark_all_as_read")
        self.assertEqual(resolve(url).view_name, "users:mark_all_as_read")
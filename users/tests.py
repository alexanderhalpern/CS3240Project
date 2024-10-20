from django.test import TestCase

import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Project, File

class FileUploadTest(TestCase):

    def setUp(self):
        #mocks user
        self.user = User.objects.create_user(username='jonfox', password='bigbrain9')
        self.client.login(username='jonfox', password='bigbrain9')  #logs user in
        
        #mocks project
        self.project = Project.objects.create(name='Jon Project', description='Jon code', created_by=self.user)

    def tearDown(self):
        #since the test always creates an example file, this helper function just removes it
        for uploaded_file in File.objects.all():
            if uploaded_file.file:
                file_path = uploaded_file.file.path
                if os.path.exists(file_path):
                    os.remove(file_path) #deletes file
        super().tearDown()

    def test_for_successful_upload(self):
        #if the request turns 200, the test passes
        my_test_file = SimpleUploadedFile("jonproj.txt", b"jon code", content_type="text/plain")
        response = self.client.post(reverse('users:project-files', kwargs={'id': self.project.id}), {
            'file': my_test_file
        }, follow=True)
        self.assertEqual(response.status_code, 200, "the upload did not return 200 success")

    def test_if_file_in_database(self):
        #if the file is in database after uploading, test passes
        my_test_file = SimpleUploadedFile("jonproj.txt", b"jon code", content_type="text/plain")
        self.client.post(reverse('users:project-files', kwargs={'id': self.project.id}), {
            'file': my_test_file
        }, follow=True)
        self.assertEqual(File.objects.count(), 1, "file was not found in database")

    def test_file_associated_with_correct_project(self):
        #if the uploaded file is associated with the correct project, the test passes
        my_test_file = SimpleUploadedFile("jonproj.txt", b"jon code", content_type="text/plain")
        self.client.post(reverse('users:project-files', kwargs={'id': self.project.id}), {
            'file': my_test_file
        }, follow=True)
        my_uploaded_file = File.objects.first()
        self.assertEqual(my_uploaded_file.project, self.project, "file is not associated with correct project")

    def test_uploaded_file_name(self):
        #test if uploaded file has correct name
        my_test_file = SimpleUploadedFile("jonproj.txt", b"jon code", content_type="text/plain")
        self.client.post(reverse('users:project-files', kwargs={'id': self.project.id}), {
            'file': my_test_file
        }, follow=True)
        my_uploaded_file = File.objects.first()
        my_uploaded_file_name = os.path.basename(my_uploaded_file.file.name)
        self.assertTrue(my_uploaded_file_name.startswith('jonproj'),
                        f"the file name is not correct: {my_uploaded_file_name}")
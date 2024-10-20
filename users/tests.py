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

    def test_file_upload(self):
        #mocks a file for uploading
        test_if_file_uploaded = SimpleUploadedFile("jonproj.txt", b"jon code", content_type="text/plain")

        #send POST request to project-files in order to upload file
        response = self.client.post(reverse('users:project-files', kwargs={'id': self.project.id}), {
            'file': test_if_file_uploaded
        }, follow=True)

        #if the database response is 200, test passes
        self.assertEqual(response.status_code, 200)

        #if only one file is uploaded, test passes
        self.assertEqual(File.objects.count(), 1)
        
        #if the file is associated with correct project, test passes
        my_uploaded_file = File.objects.first()
        self.assertEqual(my_uploaded_file.project, self.project)

        #if the file has the correct name, the test passes
        my_uploaded_file_name = os.path.basename(my_uploaded_file.file.name)  #takes the filename without extension
        self.assertTrue(my_uploaded_file_name.startswith('jonproj'), 
                        f"Incorrect name found, '{my_uploaded_file_name}' jonproj not found")

        #if the file shows up in files list, test passes
        self.assertContains(response, 'jonproj.txt')
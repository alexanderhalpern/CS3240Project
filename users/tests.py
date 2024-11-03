import datetime
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
    
    def test_correct_timestamp(self):
        self.client.post(
            reverse('users:project-files', kwargs={'id': self.project.id}),
            self.test_file_data,
            follow=True
        )
        my_uploaded_file = File.objects.first()
        
        self.assertIsNotNone(my_uploaded_file.upload_date, "Upload date was not set")
        time_diff = datetime.now().timestamp() - my_uploaded_file.upload_date.timestamp()
        self.assertTrue(time_diff < 60, "Upload timestamp is not recent")

    def test_correct_file_metadata(self):
        self.client.post(
            reverse('users:project-files', kwargs={'id': self.project.id}),
            self.test_file_data,
            follow=True
        )
        my_uploaded_file = File.objects.first()
        
        self.assertEqual(my_uploaded_file.title, 'Test Document',
                        "Title was not correctly saved")
        self.assertEqual(my_uploaded_file.description, 'This is a test document',
                        "Description was not correctly saved")
        self.assertEqual(my_uploaded_file.keywords, 'test,document,upload',
                        "Keywords were not correctly saved")

    def test_correct_file_size(self):
        self.client.post(
            reverse('users:project-files', kwargs={'id': self.project.id}),
            self.test_file_data,
            follow=True
        )
        my_uploaded_file = File.objects.first()
        
        self.assertEqual(my_uploaded_file.file_size, len(b"jon code"),
                        "File size was not correctly saved in the database")
    
    def test_correct_file_type(self):
        self.client.post(
            reverse('users:project-files', kwargs={'id': self.project.id}),
            self.test_file_data,
            follow=True
        )
        my_uploaded_file = File.objects.first()
        
        self.assertEqual(my_uploaded_file.file_type, "txt",
                        "File type was not correctly saved in the database")

    def test_missing_required_fields(self):
        #testing without a title
        invalid_data = self.test_file_data.copy()
        invalid_data.pop('title')
        response = self.client.post(
            reverse('users:project-files', kwargs={'id': self.project.id}),
            invalid_data,
            follow=True
        )
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_correct_club_membership(self):
        #create non-member user
        non_member = User.objects.create_user(username='nonmember', password='password123')
        self.client.logout()
        self.client.login(username='nonmember', password='password123')
        
        response = self.client.post(
            reverse('users:project-files', kwargs={'id': self.project.id}),
            self.test_file_data,
            follow=True
        )
        
        self.assertNotEqual(response.status_code, 200,
                          "Non-member was able to upload file to project")

    def test_keyword_search(self):
        #instantiate dummy files with multiple keywords
        files_data = [
            {**self.test_file_data, 'keywords': 'python,django,test'},
            {**self.test_file_data, 'keywords': 'python,upload'},
            {**self.test_file_data, 'keywords': 'test,upload'}
        ]
        
        for file_data in files_data:
            file_data['file'] = SimpleUploadedFile(
                "test.txt", 
                b"test content", 
                content_type="text/plain"
            )
            self.client.post(
                reverse('users:project-files', kwargs={'id': self.project.id}),
                file_data,
                follow=True
            )
        
        #tests if files are retrieved with "python" as the keyword
        response = self.client.get(
            reverse('users:project-files', kwargs={'id': self.project.id}) + '?keyword=python'
        )
        self.assertEqual(len(response.context['files']), 2,
                        "Keyword search did not return correct number of files")

        

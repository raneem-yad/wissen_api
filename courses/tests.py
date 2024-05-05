from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from instructor.models import Instructor
from .models import Course
from rest_framework import status
from rest_framework.test import APITestCase


class CourseListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_courses(self):
        # create dummy image
        with open("./readme/swagger.png", "rb") as f:
            image_content = f.read()

        image = SimpleUploadedFile(
            "./readme/swagger.png", image_content, content_type="image/png"
        )

        adam = User.objects.get(username='adam')
        Course.objects.create(teacher=adam, course_name='a title', summary='test', description="test description",
                              course_requirements="test course_requirements", learning_goals="test learning_goals",
                              image=image)
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # print(response.data)
        # print(len(response.data))

    def test_logged_in_teacher_can_create_course(self):
        self.client.login(username='adam', password='pass')
        # create teacher account
        adam = User.objects.get(username='adam')
        Instructor.objects.create(owner=adam, full_name="test adam", job_title="test job title")
        teacher = Instructor.objects.get(owner=adam)
        # image again
        with open("./readme/swagger.png", "rb") as f:
            image_content = f.read()
        image = SimpleUploadedFile(
            "./readme/swagger.png", image_content, content_type="image/png"
        )

        form_data = {
            "teacher": teacher.pk,
            "course_name": "This is a test course name.",
            "summary": "These are the test course summary.",
            "description": "dummy description ",
            "course_requirements": "Test course text",
            "learning_goals": "Test course text",
            "image": image
        }

        print("Form Data:", form_data)
        response = self.client.post('/courses/', form_data)
        count = Course.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_not_logged_in_cant_create_course(self):
        response = self.client.post('/courses/', {'course_name': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseDetailViewTests(APITestCase):
    # TODO : please complete this test later when you finish all the course unit.
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Course.objects.create(
            owner=adam, title='a title', content='adams content'
        )
        Course.objects.create(
            owner=brian, title='another title', content='brians content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

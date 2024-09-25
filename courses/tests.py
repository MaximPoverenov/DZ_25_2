from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson, CourseSubscription

User = get_user_model()


class CourseLessonTests(APITestCase):

    def setUp(self):
        # Создаем пользователя и курс
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.course = Course.objects.create(title='Test Course', user=self.user)
        self.lesson = Lesson.objects.create(title='Test Lesson', description='Test Description', course=self.course)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-list')  # Замените на ваш URL
        data = {'title': 'New Lesson', 'description': 'New Description', 'course': self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})  # Замените на ваш URL
        data = {'title': 'Updated Lesson', 'description': 'Updated Description'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.id})  # Замените на ваш URL
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('course-subscribe', kwargs={'course_id': self.course.id})  # Замените на ваш URL
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        # Сначала подпишемся
        CourseSubscription.objects.create(user=self.user, course=self.course)
        url = reverse('course-unsubscribe', kwargs={'course_id': self.course.id})  # Замените на ваш URL
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CourseSubscription.objects.filter(user=self.user, course=self.course).exists())
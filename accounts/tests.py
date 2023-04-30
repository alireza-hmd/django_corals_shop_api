from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase


class CustomUserTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='test',
            email='test@example.com',
            password='test123',
        )
        cls.client = APIClient()

    def test_create_user(self):
        self.assertEqual(self.user.username, 'test')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='test123')
        self.assertEqual(superuser.username, 'admin')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_jwt_login(self):
        response = self.client.post('/accounts/auth/login/', data={'username': 'test', 'password': 'test123'})
        self.assertIn('access', response.content.decode())
        self.assertIn('refresh', response.content.decode())

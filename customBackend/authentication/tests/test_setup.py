from rest_framework.test import APITestCase
from django.urls import reverse

class TestSetUp(APITestCase):

	def setUp(self) -> None:
		self.register_url = reverse('register')
		self.login_url = reverse('login')
		self.logout_url = reverse('logout')
		
		self.user_data = {
			'username': 'User',
			'email': 'user@example.com',
			'password': 'Password'
		}
	
		return super().setUp()
	
	def tearDown(self) -> None:
		return super().tearDown()
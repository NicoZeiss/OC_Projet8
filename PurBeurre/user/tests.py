from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User


class LoginTestCase(TestCase):
	def setUp(self):
		self.credentials = {
			'username': 'myuser',
			'password': 'mypassword'
		}
		User.objects.create_user(**self.credentials)

	def test_login(self):
		response = self.client.post(reverse('user:connexion'), **self.credentials)
		user = authenticate()
		print(response.context['user'])
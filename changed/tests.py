from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout as auth_logout

# Create your tests here.
class AuthTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='TestUsername',password= 'TestPassword')



    def test_login(self):
        #test_user = User.objects.create(username="TestUsername", password = "TestPassword")
        user = User.objects.get(username='TestUsername')
        data = {
            'username': user.username,
            'password': user.password,
        }
        response = self.client.post(reverse('changed:authenticate'),data)
        self.assertTrue(user.is_authenticated)
        

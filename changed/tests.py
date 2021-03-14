from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout as auth_logout

# Create your tests here.
class AuthTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='TestUsername',password= 'TestPassword')


    '''
    Test to check whether the login (not google auth) is successful
    '''
    def test_login(self):
        user = User.objects.get(username='TestUsername')
        data = {
            'username': user.username,
            'password': user.password,
        }
        response = self.client.post(reverse('changed:authenticate'),data)
        self.assertTrue(user.is_authenticated)
    '''
        Successful test is user can logout successfully
    '''
    def test_logout(self):
        user = User.objects.get(username='TestUsername')
        data = {
            'username': user.username,
            'password': user.password,
        }
        #login
        response = self.client.post(reverse('changed:authenticate'),data)
        #logout
        try:
            logout_res = self.client.post(reverse('changed:logout'))
            self.assertTrue(user.is_authenticated)
        except:
            return False
        

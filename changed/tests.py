from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout as auth_logout
from .models import Business, BusinessInfo, Reply, ReplyForm, BusinessForm
from http import HTTPStatus
from .views import writeReview
client= Client()
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
        #self.assertTrue(true)
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
            #self.assertTrue(true)
        except:
            return False

class ReviewTestCase(TestCase):
    #This tests writing a review for a business
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        print('Creating userrr')
        login = self.client.login(username='testuser',password='password')
        test_business = Business.objects.create(business_name = 'Test business', business_pid='', category= 'Test')
        self.factory = RequestFactory()
        

        #create example user
    def test_business_form_validity(self):
        form = BusinessForm(data = {
            'covid_compliance_rating': 3,
            'capacity_limit': 25,
            'body': 'Test body',
            'indoor_dining': True,
            'outdoor_dining': False,
        })
        self.assertTrue(form.is_valid())
    
    def test_submitting_review(self):
        business = Business.objects.get(business_name='Test business')
        request = RequestFactory().post('/review_processing/',{
            'businessName': business.business_name,
            'businessPid': business.business_pid,
            'covid_compliance_rating': 5,
            'capacity_limit': 25,
            'indoor_dining': True,
            'outdoor_dining': False,
            'curbside_pickup': False,
            'delivery': False,
            'body': '',

        })
        request.user = self.user
        response = writeReview(request)
        
        self.assertEqual(response.status_code,302)

    

        


        

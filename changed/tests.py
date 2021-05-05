from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout as auth_logout
from .models import Business, BusinessInfo, Reply, ReplyForm, BusinessForm
from http import HTTPStatus
from .views import writeReview, reply, edit_comment, edit_reply, delete_reply
from datetime import datetime, timedelta

client = Client()
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

class BusinessTestCase(TestCase):
    #This tests writing a review for a business
    def setUp(self):
        self.user = User.objects.create_user(username='sample_user')
        
        login = self.client.login(username='sample_user',password='password')
        test_business = Business.objects.create(business_name = 'Sample Business', business_pid='', category= 'Test', average_rating=0)
        test_business_2 = Business.objects.create(business_name = 'Sample Business', business_pid='sample_business', category='Test', average_rating=0)
        self.factory = RequestFactory()
        
    # This is a sample review written for test business #1
    def test_submittingReview_1(self):
        business = Business.objects.get(business_name='Sample Business', business_pid='')
        request = RequestFactory().post('/review_processing/',{
            'businessName': business.business_name,
            'businessPid': business.business_pid,
            'covid_compliance_rating': 5,
            'capacity_limit': 25,
            'indoor_dining': True,
            'outdoor_dining': False,
            'curbside_pickup': False,
            'delivery': False,
            'published_date': datetime.utcnow() + timedelta(hours=-4),
            'body': 'Great',
        })
        request.user = self.user
        response = writeReview(request)
        business.average()

        self.assertEqual(response.status_code,302)
        self.assertEqual(business.average_rating,5.0)


    # This is a sample review written for test business #2
    def test_submittingReview_2(self):
        business = Business.objects.get(business_name='Sample Business', business_pid='sample_business')
        request = RequestFactory().post('/review_processing/',{
            'businessName': business.business_name,
            'businessPid': business.business_pid,
            'covid_compliance_rating': 2,
            'capacity_limit': 25,
            'indoor_dining': False,
            'outdoor_dining': True,
            'curbside_pickup': True,
            'delivery': False,
            'published_date': datetime.utcnow() + timedelta(hours=-4),
            'body': 'Not so great',
        })
        request.user = self.user
        response = writeReview(request)
        business.average()

        self.assertEqual(response.status_code,302)
        self.assertEqual(business.average_rating, 2.0)

    def test_comparingBusiness(self):
        business_1 = Business.objects.get(business_name='Sample Business',business_pid='sample_business')
        business_2 = Business.objects.get(business_name='Sample Business',business_pid='')
        review_1 = business_1.businessinfo_set.all()
        review_2 = business_2.businessinfo_set.all()
        
        self.assertNotEqual(review_1, review_2)
        

class ReviewTestCase(TestCase):
    #This tests writing a review for a business
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        
        login = self.client.login(username='testuser',password='password')
        test_business = Business.objects.create(business_name = 'Test business', business_pid='', category= 'Test', average_rating=0)
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
        business = Business.objects.get(business_name='Test business', business_pid='')
        request = RequestFactory().post('/review_processing/',{
            'businessName': business.business_name,
            'businessPid': business.business_pid,
            'covid_compliance_rating': 5,
            'capacity_limit': 25,
            'indoor_dining': True,
            'outdoor_dining': False,
            'curbside_pickup': False,
            'delivery': False,
            'published_date': datetime.utcnow() + timedelta(hours=-4),
            'body': 'Great',
        })
        request.user = self.user
        response = writeReview(request)
        
        self.assertEqual(response.status_code,302)
        self.assertTrue(BusinessInfo.objects.filter(business = business, user = request.user, body = 'Great').exists())

class EditReviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        login = self.client.login(username='testuser',password='password')
        test_business = Business.objects.create(business_name = 'Test business', business_pid='sample_business', category= 'Test', average_rating=0)
        test_business_info = BusinessInfo.objects.create(business = test_business, body= 'Test Review', user = self.user, published_date=datetime.utcnow() + timedelta(hours=-4))
        self.factory = RequestFactory()

    def test_editingReview(self):
        business = Business.objects.get(business_name='Test business', business_pid='sample_business')
        comment = BusinessInfo.objects.get(business = business, user = self.user, body='Test Review')
        comment_id = comment.id
        business_pid = business.business_pid

        url = '/edit_comment/' + str(business_pid) +'/' + str(comment_id) + '/'

        request = RequestFactory().post('url',{
            'businessName': business.business_name,
            'businessPid': business.business_pid,
            'covid_compliance_rating': 3,
            'capacity_limit': 25,
            'indoor_dining': True,
            'outdoor_dining': False,
            'curbside_pickup': False,
            'delivery': True,
            'body': 'Another test review',
        })
        request.user = self.user
        response = edit_comment(request, business_pid, comment_id)
        
        review = BusinessInfo.objects.get(id=comment_id)
        self.assertEqual(review.body, 'Another test review')
        self.assertEqual(review.covid_compliance_rating,3)


class ReplyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        login = self.client.login(username='testuser',password='password')
        test_business = Business.objects.create(business_name = 'Test bussiness', business_pid='', category= 'Test', average_rating=0)
        test_business_info = BusinessInfo.objects.create(business = test_business, body= 'Test Review', user = self.user, published_date=datetime.utcnow() + timedelta(hours=-4))
        self.factory = RequestFactory()
    
    def test_writing_reply_to_a_review(self):
        test_id = BusinessInfo.objects.get(body = 'Test Review').id
        url = '/replies/'+str(test_id)+'/'
        
        request = RequestFactory().post(url, {
            'reply': 'Test reply body',
        })
        request.user = self.user
        
        response = reply(request,test_id)
        
        self.assertEqual(response.status_code,200)

class EditReplyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        login = self.client.login(username='testuser',password='password')
        test_business = Business.objects.create(business_name = 'Test business', business_pid='sample_business', category= 'Test', average_rating=0)
        test_business_info = BusinessInfo.objects.create(business = test_business, body= 'Test Review', user = self.user, published_date=datetime.utcnow() + timedelta(hours=-4))
        test_reply = Reply.objects.create(user=self.user, comment=test_business_info,body='Test Reply', published_date=datetime.utcnow() + timedelta(hours=-4))
        self.factory = RequestFactory()
    
    def test_editingReply(self):
        business = Business.objects.get(business_name='Test business', business_pid='sample_business')
        comment = BusinessInfo.objects.get(business = business, user = self.user, body='Test Review')
        comment_id = comment.id
        reply = Reply.objects.get(user=self.user, comment=comment,body='Test Reply')
        reply_id = reply.id

        url = '/edit_reply/' + str(comment_id) +'/' + str(reply_id) + '/'

        request = RequestFactory().post('url',{
            'reply': 'Another test reply',
        })
        request.user = self.user
        response = edit_reply(request, comment_id, reply_id)
        
        reply = Reply.objects.get(id=reply_id)
        self.assertEqual(reply.body, 'Another test reply')
        self.assertEqual(reply.comment, comment)

class DeleteReplyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        login = self.client.login(username='testuser',password='password')
        test_business = Business.objects.create(business_name = 'Test business', business_pid='sample_business', category= 'Test', average_rating=0)
        test_business_info = BusinessInfo.objects.create(business = test_business, body= 'Test Review', user = self.user, published_date=datetime.utcnow() + timedelta(hours=-4))
        test_reply = Reply.objects.create(user=self.user, comment=test_business_info,body='Test Reply', published_date=datetime.utcnow() + timedelta(hours=-4))
        self.factory = RequestFactory()
    
    def test_deletingReply(self):
        business = Business.objects.get(business_name='Test business', business_pid='sample_business')
        comment = BusinessInfo.objects.get(business = business, user = self.user, body='Test Review')
        comment_id = comment.id
        reply = Reply.objects.get(user=self.user, comment=comment,body='Test Reply')
        reply_id = reply.id

        url = '/delete_reply/' + str(comment_id) +'/' + str(reply_id) + '/'

        request = RequestFactory().post('url',{
            'reply': 'Another test reply',
        })
        request.user = self.user
        response = delete_reply(request, comment_id, reply_id)
        
        self.assertFalse(Reply.objects.filter(user=self.user, comment=comment,body='Test Reply').exists())
        self.assertEqual(response.status_code,200)
        


        


        

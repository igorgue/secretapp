from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from models import *

class SecretTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user', password='x')
        self.client.login(username='user', password='x')
    
    def test_search(self):
        # TODO
        pass
        
    def test_view(self):
        
        pass
    
    def test_edit(self):
        
        pass
    
#    def test_login(self):
#        URL = reverse('login')
#        
#        # Test bad-form
#        POST = { 'email': '', 'password': '' }
#        response = self.client.post('/login/', POST)
#        self.failUnlessEqual(response.status_code, 200)
#        for f in ['email','password']:
#            self.assertFormError(response, 'form', f, ERRORS['required'])
#        
#        # Test bad-user
#        POST = { 'email': 'x@test.com', 'password': 'word' }
#        response = self.client.post(URL, POST)
#        self.failUnlessEqual(response.status_code, 200)
#        self.assertFormError(response, 'form', None, ERRORS['no_user'])
#        
#        POST = { 'email': TEST_LOGIN, 'password': 'word' }
#        response = self.client.post(URL, POST)
#        self.failUnlessEqual(response.status_code, 200)
#        self.assertFormError(response, 'form', None, ERRORS['bad_login'])
#        
#        # Test good-user
#        POST = { 'email': TEST_LOGIN, 'password': TEST_PASSWORD }
#        response = self.client.post(URL, POST)
#        self.failUnlessEqual(response.status_code, 302)
#        REDIRECT = reverse('home')
#        self.assertRedirects(response, REDIRECT)
#        response = self.client.get(REDIRECT)
#        self.assertEqual(response.context[-1]['user'].email, POST['email'])
#    
#    def test_logout(self):
#        URL = reverse('logout')
#        
#        # is logged in
#        self.client.login(username=TEST_LOGIN, password=TEST_PASSWORD)
#        
#        # goes to logout page
#        response = self.client.get(URL)
#        REDIRECT = reverse('home')
#        self.assertRedirects(response, REDIRECT)
#        response = self.client.get(REDIRECT)
#        self.failIf(response.context[-1]['user'].is_authenticated())
#        
#    
#    def test_signup(self):
#        URL = reverse('signup')
#        
#        # Test bad-form
#        POST = {'email': '', 'password': '', 'first_name': '', 'last_name': ''}
#        response = self.client.post(URL, POST)
#        self.failUnlessEqual(response.status_code, 200)
#        for f in ['email','password','first_name','last_name']:
#            self.assertFormError(response, 'form', f, ERRORS['required'])
#        
#        # Test user-exists
#        POST = {
#            'email': TEST_LOGIN,
#            'password': TEST_PASSWORD,
#            'first_name': 'john',
#            'last_name': 'smith',
#        }
#        response = self.client.post(URL, POST)
#        self.failUnlessEqual(response.status_code, 200)
#        self.assertFormError(response, 'form', 'email', ERRORS['already_user'])
#        
#        # Test good (non-existing) user
#        POST = {
#            'email': 'jsmith@mail.com',
#            'password': 'hotminute',
#            'first_name': 'john',
#            'last_name': 'smith',
#        }
#        response = self.client.post(URL, POST)
#        self.failUnlessEqual(response.status_code, 302)
#        REDIRECT = reverse('home')
#        self.assertRedirects(response, REDIRECT)
#        response = self.client.get(REDIRECT)
#        self.assertEqual(response.context[-1]['user'].email, POST['email'])
#    


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse


class TestModifyEmailPage(StaticLiveServerTestCase):

    def setUp(self):
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@gmail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        
        self.browser = webdriver.Chrome('functional_tests/chromedriver')
        login_url = self.live_server_url + reverse('user:connexion')
        self.browser.get(login_url)
        username = self.browser.find_element_by_id('username')
        password = self.browser.find_element_by_id('password')
        submit = self.browser.find_element_by_id('submit-button')
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.send_keys(Keys.RETURN)

    def tearDown(self):
        self.browser.close()

    def test_modify_email_works(self):
        account_url = self.live_server_url + reverse('user:account')
        self.browser.get(account_url)
        new_email = self.browser.find_element_by_id('new-email')
        submit = self.browser.find_element_by_id('submit-button')
        new_email.send_keys('newmail@gmail.com')
        submit.send_keys(Keys.RETURN)
        user = User.objects.get(username=self.username)
        self.assertEquals(user.email, 'newmail@gmail.com')

    def test_wrong_email_raise_error(self):
        account_url = self.live_server_url + reverse('user:account')
        response = self.browser.get(account_url)
        new_email = self.browser.find_element_by_id('new-email')
        submit = self.browser.find_element_by_id('submit-button')
        new_email.send_keys('newmail@gmail')
        submit.send_keys(Keys.RETURN)
        self.assertIn("Saisissez une adresse de courriel valide", self.browser.page_source)
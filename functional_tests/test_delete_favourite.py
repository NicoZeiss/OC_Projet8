from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from comparator.models import Food, Category
from django.contrib.auth import authenticate
from django.urls import reverse
import time


class TestDeleteFavouritePage(StaticLiveServerTestCase):

    def setUp(self):
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@gmail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()
        category = Category.objects.create(name="MyCat")
        self.food = Food.objects.create(code="7", name="MyFood", category_id=category.id)
        self.user.food.add(self.food)

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

    def test_favourite_is_deleted_from_fav_temp(self):
        favourites_url = self.live_server_url + reverse('comparator:favourites')
        self.browser.get(favourites_url)
        submit = self.browser.find_element_by_id("func-test")
        submit.send_keys(Keys.RETURN)
        self.assertNotIn(self.food, self.user.food.all())
        self.assertNotIn("MyFood", self.browser.page_source)

    def test_favourite_is_deleted_from_sub_temp(self):
        substitute_url = '{}?{}={}'.format(self.live_server_url + reverse('comparator:substitute'), 'user_substitute', self.food.code)
        self.browser.get(substitute_url)
        submit = self.browser.find_element_by_id("func-test")
        submit.send_keys(Keys.RETURN)
        self.assertNotIn(self.food, self.user.food.all())
        self.assertIn("Ajouter aux favoris", self.browser.page_source)
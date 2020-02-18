"""Here are all the tests (unit and intregrating) concerning comaprator app"""


from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Food, Category
from .init_db import populate_categories


#########################################################################
#   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   #
########################################################################


class IndexViewTestCase(TestCase):
    """Testing index page"""

    def test_index_view(self):
        """We test 200 returns + template used"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/index.html')


class DetailViewTestCase(TestCase):
    """Testing detail page"""

    def setUp(self):
        category = Category.objects.create(name="MyCat")
        cat_id = category.id
        self.food = Food.objects.create(code="7", name="MyFood", category_id=cat_id)

    def test_detail_view_returns_200(self):
        """We test that detail view returns a 200 if the item exists"""
        code = self.food.code
        response = self.client.get(reverse('comparator:detail', args=(code)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/detail.html')

    def test_detail_view_returns_404(self):
        """We test that detail view returns a 404 if the item doesn't exist"""
        code = str(int(self.food.code) + 1)
        response = self.client.get(reverse('comparator:detail', args=(code)))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')


class TermsViewTestCase(TestCase):
    """Testing terms page"""

    def test_terms_view(self):
        """We test 200 returns + template used"""
        response = self.client.get(reverse('comparator:terms'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/terms.html')


class SearchViewTestCase(TestCase):
    """Testing search page"""

    def setUp(self):
        category = Category.objects.create(name="MyCat")
        cat_id = category.id
        self.food = Food.objects.create(code="7", name="MyFood", category_id=cat_id)

    def test_search_view_returns_200(self):
        """We test that search view returns 200 and item is
        displayed on html when query has results"""
        query = "food"
        result_list = Food.objects.filter(name__icontains=query).order_by('code')
        url = '{}?{}={}'.format(reverse('comparator:search'), 'user_input', query)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/search.html')
        for item in result_list:
            self.assertIn(item.name, str(response.content))

    def test_search_view_returns_200_with_wrong_request(self):
        """We test that search views returns 200 and display
        a failure mess when query hasn't result"""
        query = "fffff"
        url = '{}?user_input={}'.format(reverse('comparator:search'), query)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/search.html')
        self.assertIn("Aucun r\\xc3\\xa9sultat de recherche", str(response.content))

    def test_paginator_active(self):
        """We test that paginator is active"""
        query = "food"
        url = '{}?{}={}'.format(reverse('comparator:search'), 'user_input', query)
        response = self.client.get(url)
        self.assertEqual(response.context['paginate'], True)


class SubstituteViewTestCase(TestCase):
    """Testing substitute page"""

    def setUp(self):
        category = Category.objects.create(name="MyCat")
        cat_id = category.id
        Food.objects.create(code="10", name="cat", nutriscore="a", category_id=cat_id)
        Food.objects.create(code="20", name="dog", nutriscore="b", category_id=cat_id)
        Food.objects.create(code="30", name="duck", nutriscore="b", category_id=cat_id)
        Food.objects.create(code="40", name="horse", nutriscore="d", category_id=cat_id)
        Food.objects.create(code="50", name="bee", nutriscore="a", category_id=cat_id)
        Food.objects.create(code="60", name="cow", nutriscore="a", category_id=cat_id)
        Food.objects.create(code="70", name="bird", nutriscore="a", category_id=cat_id)
        Food.objects.create(code="80", name="fish", nutriscore="c", category_id=cat_id)
        Food.objects.create(code="90", name="sheep", nutriscore="c", category_id=cat_id)
        Food.objects.create(code="100", name="spider", nutriscore="e", category_id=cat_id)
        self.item = Food.objects.get(name="duck")

    def test_substitute_returns_200(self):
        """We test that substitute view returns 200 if the item exists"""
        code = self.item.code
        url = '{}?{}={}'.format(reverse('comparator:substitute'), 'user_substitute', code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/substitute.html')

    def test_substitute_returns_404(self):
        """We test that substitute view returns 404 if the item does not exist"""
        code = str(int(self.item.code) + 1)
        url = '{}?{}={}'.format(reverse('comparator:substitute'), 'user_substitute', code)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    def test_search_view_returns_200(self):
        """We test that substitute view displayed 9 better items on html template"""
        code = self.item.code
        result_list = Food.objects.filter(category_id=self.item.category_id).order_by('nutriscore')
        url = '{}?{}={}'.format(reverse('comparator:substitute'), 'user_substitute', code)
        response = self.client.get(url)
        i = 0
        while i <= 8:
            item = result_list[i]
            self.assertIn(item.name, str(response.content))
            i += 1


class InitDbTestCase(TestCase):
    """We test the script which create the database"""

    def setUp(self):
        self.test_cat = ["porridges"]

    def test_create_db(self):
        """run script and test if table exists in temp db"""
        populate_categories(self.test_cat)
        cat_name = Category.objects.get()
        self.assertEqual(cat_name.name, self.test_cat[0])


##################################################################################
#   INTEGRATION TESTING   ##   INTEGRATION TESTING   ##   INTEGRATION TESTING   #
#################################################################################


class SaveSubViewTestCase(TestCase):
    """We test that user can save food as substitute"""

    def setUp(self):
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@mail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        category = Category.objects.create(name="MyCat")
        cat_id = category.id
        self.food = Food.objects.create(code="7", name="MyFood", category_id=cat_id)
        self.substitute = Food.objects.create(code="8", name="MySubstitute", category_id=cat_id)

    def test_save_substitute(self):
        """If substitute is saved, user is redirected to sub result from his query"""
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        food_code = self.food.code
        sub_code = self.substitute.code
        response = self.client.get(reverse('comparator:save_sub'), {
            'query_code': food_code,
            'sub_code': sub_code
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/comparator/substitute/?user_substitute=7")
        self.assertIn(self.substitute, self.user.food.all())

    def test_sub_not_auth_redirect_connexion(self):
        """If user is not authenticated, he's redirected to connexion page"""
        food_code = self.food.code
        sub_code = self.substitute.code
        response = self.client.get(reverse('comparator:save_sub'), {
            'query_code': food_code,
            'sub_code': sub_code
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user/connexion/")


class FavouritesViewTestCase(TestCase):
    """Testing favourites view"""
    def setUp(self):
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@mail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

        category = Category.objects.create(name="MyCat")
        cat_id = category.id
        items = [
            {'code': "10", 'name': "cat", 'nutriscore': "a"},
            {'code': "20", 'name': "dog", 'nutriscore': "b"},
            {'code': "30", 'name': "duck", 'nutriscore': "b"},
            {'code': "40", 'name': "horse", 'nutriscore': "d"},
            {'code': "50", 'name': "bee", 'nutriscore': "a"},
            {'code': "60", 'name': "cow", 'nutriscore': "a"},
            {'code': "70", 'name': "bird", 'nutriscore': "a"},
            {'code': "80", 'name': "fish", 'nutriscore': "c"},
            {'code': "90", 'name': "sheep", 'nutriscore': "c"},
            {'code': "100", 'name': "spider", 'nutriscore': "d"},
        ]
        for item in items:
            favourite = Food.objects.create(code=item['code'], name=item['name'], nutriscore=item['nutriscore'], category_id=cat_id)
            self.user.food.add(favourite)

    def test_favourites_view(self):
        """We test that view returns 200 and fav template when user is authenticated"""
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('comparator:favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparator/favourites.html')

    def test_fav_not_auth_redirect_connexion(self):
        """We test that user is redirected to connexion page if he's not connected"""
        response = self.client.get(reverse('comparator:favourites'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user/connexion/")

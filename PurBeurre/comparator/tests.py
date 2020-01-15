from django.shortcuts import reverse
from django.test import TestCase
from .models import Food, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


##########################################################################################
#   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   #
##########################################################################################


# Index view
class IndexViewTestCase(TestCase):
	def test_index_view(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'comparator/index.html')


# Detail view
class DetailViewTestCase(TestCase):
	def setUp(self):
		category = Category.objects.create(name="MyCat")
		cat_id = category.id
		food = Food.objects.create(code="7", name="MyFood", category_id=cat_id)
		self.item = Food.objects.get(name="MyFood")

	# We test that detail view returns a 200 if the item exists
	def test_detail_view_returns_200(self):
		code = self.item.code
		response = self.client.get(reverse('comparator:detail', args=(code)))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'comparator/detail.html')

	# We test that detail view returns a 404 if the item doesn't exist
	def test_detail_view_returns_404(self):
		code = str(int(self.item.code) + 1)
		response = self.client.get(reverse('comparator:detail', args=(code)))
		self.assertEqual(response.status_code, 404)
		self.assertTemplateUsed(response, '404.html')


# Terms view
class TermsViewTestCase(TestCase):
	def test_terms_view(self):
		response = self.client.get(reverse('comparator:terms'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'comparator/terms.html')


# Search view
class SearchViewTestCase(TestCase):
	def setUp(self):
		category = Category.objects.create(name="MyCat")
		cat_id = category.id
		food = Food.objects.create(code="7", name="MyFood", category_id=cat_id)
		self.item = Food.objects.get(name="MyFood")

	# We test that search view returns 200 and item is displayed on html template when query has results
	def test_search_view_returns_200(self):
		query = "food"
		result_list = Food.objects.filter(name__icontains=query).order_by('code')
		url = '{}?{}={}'.format(reverse('comparator:search'), 'user_input', query)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'comparator/search.html')
		for item in result_list:
			self.assertIn(item.name, str(response.content))

	# We test that search views returns 200 and html display a failure message when query has not result
	def test_search_view_returns_200_with_wrong_request(self):
		query = "fffff"
		url = '{}?user_input={}'.format(reverse('comparator:search'), query)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'comparator/search.html')
		self.assertIn("Aucun r\\xc3\\xa9sultat de recherche", str(response.content))

	# We test that paginator is active
	def test_paginator_active(self):
		query = "food"
		url = '{}?{}={}'.format(reverse('comparator:search'), 'user_input', query)
		response = self.client.get(url)
		self.assertEqual(response.context['paginate'], True)


# Substitute view
class SubstituteViewTestCase(TestCase):
	def setUp(self):
		category = Category.objects.create(name="MyCat")
		cat_id = category.id
		cat = Food.objects.create(code="10", name="cat", nutriscore="a", category_id=cat_id)
		dog = Food.objects.create(code="20", name="dog", nutriscore="b", category_id=cat_id)
		duck = Food.objects.create(code="30", name="duck", nutriscore="b", category_id=cat_id)
		horse = Food.objects.create(code="40", name="horse", nutriscore="d", category_id=cat_id)
		bee = Food.objects.create(code="50", name="bee", nutriscore="a", category_id=cat_id)
		cow = Food.objects.create(code="60", name="cow", nutriscore="a", category_id=cat_id)
		bird = Food.objects.create(code="70", name="bird", nutriscore="a", category_id=cat_id)
		fish = Food.objects.create(code="80", name="fish", nutriscore="c", category_id=cat_id)
		sheep = Food.objects.create(code="90", name="sheep", nutriscore="c", category_id=cat_id)
		spider = Food.objects.create(code="100", name="spider", nutriscore="e", category_id=cat_id)
		self.item = Food.objects.get(name="duck")

	# We test that substitute view returns 200 if the item exists
	def test_substitute_returns_200(self):
		code = self.item.code
		url = '{}?{}={}'.format(reverse('comparator:substitute'), 'user_substitute', code)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'comparator/substitute.html')

	# We test that substitute view returns 404 if the item does not exist
	def test_substitute_returns_404(self):
		code = str(int(self.item.code) + 1)
		url = '{}?{}={}'.format(reverse('comparator:substitute'), 'user_substitute', code)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)
		self.assertTemplateUsed(response, '404.html')

	# We test that substitute view displayed 9 better items on html template
	def test_search_view_returns_200(self):
		code = self.item.code
		result_list = Food.objects.filter(category_id=self.item.category_id).order_by('nutriscore')
		url = '{}?{}={}'.format(reverse('comparator:substitute'), 'user_substitute', code)
		response = self.client.get(url)
		i = 0
		while i <= 8:
			item = result_list[i]
			self.assertIn(item.name, str(response.content))
			i += 1


#######################################################################################################################################
#   INTEGRATION TESTING   ##   INTEGRATION TESTING   ##   INTEGRATION TESTING   ##   INTEGRATION TESTING   ##   INTEGRATION TESTING   #
#######################################################################################################################################


# class FavouritesViewTestCase(TestCase):
# 	def setUp(self):
# 		self.user = User.objects.create_user("MyUser", "mymail@mail.com", "whatapassword")
# 		self.username = self.user.username
# 		self.password = self.user.password

# 	def test_favourites_view_authenticated(self):
# 		user = authenticate(username=self.username, password=self.password)
# 		login(user)
# 		response = self.client.get(reverse('comparator:favourites'))
# 		print(response)
# 		self.assertTrue(user_login)



from django.shortcuts import reverse
from django.test import TestCase
from .models import Food, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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
	# def setUp(self):
	# 	category = Category.objects.create(name="MyCat")
	# 	cat_id = category.id
	# 	food = Food.objects.create(code="7", name="MyFood", category_id=cat_id)
	# 	self.item = Food.objects.get(name="MyFood")

	# We test that search view returns a list and 200 when query has results
	def test_search_view_returns_200(self):
		query = "fofdfd"
		url = '{}?{}={}'.format(reverse('comparator:search'), 'user_input', query)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'comparator/search.html')


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



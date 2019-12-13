import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PurBeurre.settings")
import django
django.setup()
import requests

from comparator.models import Category, Food
from comparator.constants import categories_name, api_url, product_url, cat_url




def populate_categories():
	i = 1
	for category in categories_name:
		print("\nFeeding category [{}/{}] : {}...".format(i,len(categories_name), category))
		new_cat = Category(name=category)
		new_cat.save()
		prod_count = extract_codes_from_api(new_cat)
		print("Category {} populated with {} products!".format(category, prod_count))
		i += 1


def extract_codes_from_api(cat_obj):
	codes = []
	i = 1
	while i != 0:
		cat = requests.get("https://fr.openfoodfacts.org/categorie/" + cat_obj.name + "/" + str(i) + ".json").json()
		if len(cat["products"]) != 0:
			for item in cat["products"]:
				if len(codes) < 100:
					codes.append(item["code"])
				else:
					i = -1
					break
		else:
			break
		i += 1

	prod_count = populate_products(cat_obj, codes)
	return prod_count



def populate_products(cat_obj, codes):

	i = 1
	for code in codes:
		r = requests.get(api_url + code + ".json").json()

		try:
			new_prod = Food(code=code)
			new_prod.name = r["product"]["product_name"]
			new_prod.nutriscore = r["product"]["nutrition_grade_fr"]
			new_prod.pict = r["product"]["selected_images"]["front"]["display"]["fr"]
			new_prod.fat = r["product"]["nutriments"]["fat_100g"]
			new_prod.salt = r["product"]["nutriments"]["salt_100g"]
			new_prod.saturated_fat = r["product"]["nutriments"]["saturated-fat_100g"]
			new_prod.sugars = r["product"]["nutriments"]["sugars_100g"]
			new_prod.off_url = product_url + code
			new_prod.category = cat_obj
			new_prod.save()
			i += 1
		except:
			pass

	return i


def main():
	populate_categories()

main()
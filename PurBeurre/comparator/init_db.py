"""This script populate the database with categories and food items"""

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PurBeurre.settings")
# import django
# django.setup()


import requests

from comparator.models import Category, Food
from comparator.constants import api_url, product_url


def populate_categories(cat_name):
    """This function create all categories"""
    i = 1
    for category in cat_name:
        print("\nFeeding category [{}/{}] : {}...".format(i, len(cat_name), category))
        new_cat = Category(name=category)
        new_cat.save()
        prod_count = extract_codes_from_api(new_cat)
        print("Category {} populated with {} products!".format(category, prod_count))
        i += 1

def extract_codes_from_api(cat_obj):
    """This function extract all 100 first barcode from api
    to populate each category"""
    codes = []
    i = 1
    while i != 0:
        url = "https://fr.openfoodfacts.org/categorie/" + cat_obj.name + "/" + str(i) + ".json"
        cat = requests.get(url).json()
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
    """This function create food objects for each barcode"""
    i = 1
    for code in codes:
        api_req = requests.get(api_url + code + ".json").json()

        try:
            new_prod = Food(code=code)
            new_prod.name = api_req["product"]["product_name"]
            new_prod.nutriscore = api_req["product"]["nutrition_grade_fr"]
            new_prod.pict = api_req["product"]["selected_images"]["front"]["display"]["fr"]
            new_prod.fat = api_req["product"]["nutriments"]["fat_100g"]
            new_prod.salt = api_req["product"]["nutriments"]["salt_100g"]
            new_prod.saturated_fat = api_req["product"]["nutriments"]["saturated-fat_100g"]
            new_prod.sugars = api_req["product"]["nutriments"]["sugars_100g"]
            new_prod.off_url = product_url + code
            new_prod.category = cat_obj
            new_prod.save()
            i += 1
        except:
            pass

    return i

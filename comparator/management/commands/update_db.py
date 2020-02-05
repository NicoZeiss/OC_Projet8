"""This script do an update on the database"""


import requests

from comparator.models import Category, Food
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Update the database"

    def handle(self, *args, **options):
        categories = Category.objects.filter()
        for category in categories:
            print("\nChecking : {}\n".format(category.name))
            del_item = 0
            modif_item = 0
            add_item = 0
            products_list = []
            products = Food.objects.filter(category_id=category.id)
            for product in products:
                products_list.append(product.code)
            products_len = len(products)
            for item in products:
                modif = False
                try:
                    product_url = 'https://fr.openfoodfacts.org/api/v0/product/' + item.code + ".json"
                    api_req = requests.get(product_url).json()
                    if api_req["product"]["product_name"] != item.name:
                        item.name = api_req["product"]["product_name"]
                        modif = True
                    if api_req["product"]["nutrition_grade_fr"] != item.nutriscore:
                        item.nutriscore = api_req["product"]["nutrition_grade_fr"]
                        modif = True
                    if api_req["product"]["selected_images"]["front"]["display"]["fr"] != item.pict:
                        item.pict = api_req["product"]["selected_images"]["front"]["display"]["fr"]
                        modif = True
                    if float(round(api_req["product"]["nutriments"]["fat_100g"], 2)) != float(item.fat):
                        item.fat = api_req["product"]["nutriments"]["fat_100g"]
                        modif = True
                    if float(round(api_req["product"]["nutriments"]["salt_100g"], 2)) != float(item.salt):
                        item.salt = api_req["product"]["nutriments"]["salt_100g"]
                        modif = True
                    if float(round(api_req["product"]["nutriments"]["saturated-fat_100g"], 2)) != float(item.saturated_fat):
                        item.saturated_fat = api_req["product"]["nutriments"]["saturated-fat_100g"]
                        modif = True
                    if float(round(api_req["product"]["nutriments"]["sugars_100g"], 2)) != float(item.sugars):
                        item.sugars = api_req["product"]["nutriments"]["sugars_100g"]
                        modif = True
                    item.save()
                    if modif == True:
                        modif += 1
                except:
                    item.delete()
                    del_item += 1

            i = 1
            while i != 0:
                url = "https://fr.openfoodfacts.org/categorie/" + category.name + "/" + str(i) + ".json"
                cat = requests.get(url).json()
                if len(cat["products"]) != 0:
                    for api_prod in cat["products"]:
                        if not api_prod["code"] in products_list:
                            if products_len < 100:
                                product_url = "https://fr.openfoodfacts.org/api/v0/product/" + api_prod["code"] + ".json"
                                api_req = requests.get(product_url).json()
                                try:
                                    new_prod = Food(code=api_prod["code"])
                                    new_prod.name = api_req["product"]["product_name"]
                                    new_prod.nutriscore = api_req["product"]["nutrition_grade_fr"]
                                    new_prod.pict = api_req["product"]["selected_images"]["front"]["display"]["fr"]
                                    new_prod.fat = api_req["product"]["nutriments"]["fat_100g"]
                                    new_prod.salt = api_req["product"]["nutriments"]["salt_100g"]
                                    new_prod.saturated_fat = api_req["product"]["nutriments"]["saturated-fat_100g"]
                                    new_prod.sugars = api_req["product"]["nutriments"]["sugars_100g"]
                                    new_prod.off_url = "https://fr.openfoodfacts.org/produit/" + api_prod["code"]
                                    new_prod.category = category
                                    new_prod.save()
                                    products_len += 1
                                    add_item += 1
                                except:
                                    pass
                            else:
                                i = -1
                else:
                    break
                i += 1

            print("{} item(s) deleted".format(del_item))
            print("{} item(s) modified".format(modif_item))
            print("{} item(s) added".format(add_item))

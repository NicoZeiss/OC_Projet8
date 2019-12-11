from django.db import models

# Create your models here.

categories_name = ['boissons-energisantes', 'beignets-sucres', 'taboules', 'pates-a-tartiner', 'cafes-en-dosettes', 'cafes-decafeines', 'cafes-moulus', 'cafes-solubles', 
'popcorn', 'chips', 'biscuits-aperitifs', 'fruits-a-coques-sales', 'eaux-gazeuses', 'laits', 'cremes-fraiches', 'soupes-de-legumes', 'pains-de-mie', 'baguettes', 'cookies', 'biscuits-sables',
'gaufrettes', 'speculoos', 'jambons', 'rillettes', 'saucissons', 'boudins', 'sauves-tomate', 'moutardes', 'mayonnaises', 'sauces-au-curry', 'sauces-bechamel', 'sauces-pesto', 'sauces-salades', 'fromages-rapes',
'fromages-de-chevre', 'fromages-de-vache', 'compotes', 'glaces-a-l-eau',  'sardines', 'thons', 'maquereaux', 'anchois', 'colins', 'saumons', 'ravioli-en-conserve', 'bieres', 'liqueurs', 'cidres',
'vins-rouges', 'vins-roses', 'vins-blancs', 'yaourts-au-chocolat', 'yaourts-aux-fruits', 'yaourts-natures', 'jus-de-fruit', 'confitures', 'gratins', 'nems', 'poelees', 'filets-de-poulet', 'escalopes-de-dinde',
'steaks', 'barres-chocolatees', 'barres-energetiques', 'chocolats-noirs', 'chocolats-au-lait', 'chocolats-blancs', 'cereales-pour-petit-dejeuner'] 

class Category(models.Model):
	name = models.CharField(max_length=100)

class Food(models.Model):
	code = models.CharField(max_length=13, unique=True, primary_key=True)
	name = models.CharField(max_length=100)
	nutriscore = models.CharField(max_length=1)
	fat = models.DecimalField(max_digits=6, decimal_places=2)
	salt = models.DecimalField(max_digits=6, decimal_places=2)
	saturated_fat = models.DecimalField(max_digits=6, decimal_places=2)
	sugars = models.DecimalField(max_digits=6, decimal_places=2)
	pict = models.URLField()
	off_url = models.URLField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


def create_categories(cat_list):
	for category in cat_list:
		Category.objects.create(name=category)

def main():
	create_categories(categories_name)

main()
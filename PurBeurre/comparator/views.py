# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import CATEGORIES

def index(request):
	template = loader.get_template('comparator/index.html')
	return HttpResponse(template.render(request=request))

def listing(request):
	message = "La liste de produits ici :"
	return HttpResponse(message)

def search(request):
	query = request.GET.get('query')

	if not query:
		message = "Aucun aliment n'est demandé"
	else:
		categories = [
			categorie for categorie in CATEGORIES
			if query in " ".join(aliment['name'] for aliment in categorie['aliments'])
		]

		if len(categories) == 0:
			message = "Misère, pas de résultat trouvé"
		else:
			categories = ["<li>{}</li>".format(categorie['name']) for categorie in categories]
			message = """
				Nous avons trouvé les catégories correspondant à votre requête, les voici :
				<ul>
					{}
				</ul>
				""".format("</li><li>".join(categories))

	return HttpResponse(message)
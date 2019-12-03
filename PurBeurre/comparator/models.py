# from django.db import models

# Create your models here.

ALIMENTS = {
	'saucisson': {'name': 'Le bon saucisson'},
	'jambon': {'name': 'Le jambon qui tue'},
	'roquefort': {'name': 'Le formage trop fort'},
	'biquette': {'name': 'Le chèvre de biquette'},
}

CATEGORIES = [
	{'name': 'Viandes', 'aliments': [ALIMENTS['saucisson'], ALIMENTS['jambon']]},
	{'name': 'Fromages', 'aliments': [ALIMENTS['roquefort'], ALIMENTS['biquette']]},
]
from django.http import HttpResponse
from django.template import loader

def account(request):
	pass

def connection(request):
	template = loader.get_template('comparator/connection.html')
	return HttpResponse(template.render(request=request))

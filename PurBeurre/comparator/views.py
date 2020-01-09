import django.contrib.postgres
from django.shortcuts import render, reverse, render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import forms
from .forms import SearchForm
from .models import Food, Category


def index(request):
	form = SearchForm()
	return render(request, 'comparator/index.html', {'form': form})


def search(request):
	query = request.GET.get('user_input')
	result_list = Food.objects.filter(name__icontains=query)
	paginator = Paginator(result_list, 9)
	page = request.GET.get("page")

	try:
		food = paginator.page(page)
	except PageNotAnInteger:
		food = paginator.page(1)
	except EmptyPage:
		food = paginator.page(paginator.num_pages)

	context = {
		"user_input": query,
		"food": food,
		"paginate": True
	}	

	return render(request, 'comparator/search.html', context)

def detail(request, bar_code):
	food = Food.objects.get(code=bar_code)

	context = {
		"food": food
	}

	return render(request, 'comparator/detail.html', context)

def substitute(request):
	query = request.GET.get('user-substitute')
	user_choice = Food.objects.get(code=query)
	choice_cat = user_choice.category_id
	full_list = Food.objects.filter(category_id=choice_cat).order_by('nutriscore')
	sub_list = []
	i = 0
	while i <= 8:
		sub_list.append(full_list[i])
		i += 1

	context = {
		"sublist": sub_list,
		"query": user_choice,
	}

	return render(request, 'comparator/substitute.html', context)
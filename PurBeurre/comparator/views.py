import django.contrib.postgres
from django.shortcuts import render, reverse, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django import forms
from django.http import JsonResponse
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
	query = request.GET.get('user_substitute')
	user_choice = Food.objects.get(code=query)
	choice_cat = user_choice.category_id
	full_list = Food.objects.filter(category_id=choice_cat).order_by('nutriscore')
	sub_dic = {}
	i = 0
	while len(sub_dic) <= 8:
		food = full_list[i]
		user = request.user.id
		if len(food.user.all()) != 0:
			sub_dic[food] = True
		else:
			sub_dic[food] = False
		i += 1

	context = {
		"subdic": sub_dic,
		"query": user_choice,
	}

	return render(request, 'comparator/substitute.html', context)

def save_sub(request):
	query_code = request.GET.get('query_code')
	sub_code = request.GET.get('sub_code')
	sub = Food.objects.get(code=sub_code)
	user_id = request.user.id
	user = User.objects.get(id=user_id)
	user.food.add(sub)

	return HttpResponseRedirect('http://127.0.0.1:8000/comparator/substitute/?user_substitute={}'.format(query_code))


def favourites(request):
	user = request.user
	sub_list = user.food.all().order_by('nutriscore')
	paginator = Paginator(sub_list, 9)
	page = request.GET.get("page")

	try:
		sublist = paginator.page(page)
	except PageNotAnInteger:
		sublist = paginator.page(1)
	except EmptyPage:
		sublist = paginator.page(paginator.num_pages)


	context = {
		"sublist": sublist
	}

	return render(request, 'comparator/favourites.html', context)


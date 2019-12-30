from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms
from .forms import LoginForm, CreateUserForm
from django.core.exceptions import ValidationError


def create_user(request):
	if not request.user.is_authenticated:

		if request.method == 'POST':
			form = CreateUserForm(request.POST)

			if form.is_valid():
				username = form.cleaned_data['username']
				email = form.cleaned_data['email']
				password = form.cleaned_data['password']
				user = User.objects.create_user(username, email, password)
				user.save()
				user = authenticate(username=username, password=password)
				login(request, user)
				return HttpResponseRedirect(reverse('user:account'))

		else:
		 	form = CreateUserForm()

		return render(request, 'comparator/create_user.html', {'form': form})

	else:
		return HttpResponseRedirect(reverse('index'))


def connexion(request):

	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('user:connexion'))

			else:
				return render(request, 'comparator/login.html', {'form': form, 'error_message': 'Identifiant ou mot de passe incorrect'})

	else:
		form = LoginForm()

	return render(request, 'comparator/login.html', {'form': form})


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

def account(request):
	return render(request, 'comparator/account.html')
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from .forms import LoginForm


def create_user(request):
	pass

def connexion(request):
	error = False

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
				error = True

	else:
		form = LoginForm()

	return render(request, 'comparator/login.html', {'form': form})

def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))
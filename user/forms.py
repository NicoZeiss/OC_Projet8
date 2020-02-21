from django import forms
from .validators import unique_id, unique_email, password_min_length


class LoginForm(forms.Form):
	required_css_class = 'connect-list-row'
	username = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Identifiant', 'class': 'mytest'}))
	password = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Mot de passe', 'class': 'mytest', 'type': 'password'}))

class CreateUserForm(forms.Form):
	required_css_class = 'connect-list-row'
	username = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Identifiant', 'class': 'mytest'}), validators=[unique_id])
	email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'mytest'}), validators=[unique_email])
	password = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Mot de passe', 'class': 'mytest', 'type': 'password'}), validators=[password_min_length])

class ModifyEmailForm(forms.Form):
	email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Modifier l\'adresse email', 'class': 'mytest'}), validators=[unique_email])


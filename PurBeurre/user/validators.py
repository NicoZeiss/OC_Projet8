from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def unique_id(value):
	if User.objects.filter(username=value).exists():
		raise ValidationError('Cet identifiant existe déjà')

def unique_email(value):
	if User.objects.filter(email=value).exists():
		raise ValidationError('Cet email est déjà utilisé')

def password_min_length(value):
	if len(value) < 8:
		raise ValidationError('Le mot de passe doit contenir au moins 8 caractères')

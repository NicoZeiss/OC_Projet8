from django.db import models
from comparator.models import Food

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=30)
	connected = models.BooleanField(default=False)
	food = models.ManyToManyField(Food, related_name='user', blank=True)

	def __str__(self):
		return self.username



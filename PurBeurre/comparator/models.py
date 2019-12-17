from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class Food(models.Model):
	code = models.CharField(max_length=13, unique=True, primary_key=True)
	name = models.CharField(max_length=100)
	nutriscore = models.CharField(max_length=1)
	fat = models.DecimalField(max_digits=6, decimal_places=2, null=True)
	salt = models.DecimalField(max_digits=6, decimal_places=2, null=True)
	saturated_fat = models.DecimalField(max_digits=6, decimal_places=2, null=True)
	sugars = models.DecimalField(max_digits=6, decimal_places=2, null=True)
	pict = models.URLField()
	off_url = models.URLField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	user = models.ManyToManyField(User, related_name='food', blank=True)


	def __str__(self):
		return self.name

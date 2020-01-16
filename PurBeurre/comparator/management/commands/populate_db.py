from django.core.management.base import BaseCommand, CommandError
from django.core import management
from comparator.init_db import populate_categories
from comparator.models import Category
from comparator.constants import categories_name


class Command(BaseCommand):
	help = "Populate the database"

	# The command migrate db and populate it
	def handle(self, *args, **options):
		db_status = Category.objects.filter()
		if len(db_status) == 0:
			management.call_command('makemigrations')
			management.call_command('migrate')
			populate_categories(categories_name)
		else:
			print("Database already created")

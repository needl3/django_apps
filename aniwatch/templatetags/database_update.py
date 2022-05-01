from django.core.management import execute_from_command_line
from django.db import models
import csv

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aniwatch.settings')

def update(f):
	with open(f) as file:
		reader = csv.DictReader(file)
		for row in reader:
			pass

if __name__ == "__main__":
	update('AnimeDetails.csv')
from django.db import models

# Create your models here.
class Locations(models.Model):
	location = models.CharField(max_length=50)

	def __str__(self):
		return self.location

class LocationData(models.Model):
	location = models.ForeignKey('Locations', on_delete=models.DO_NOTHING, blank=True, null=True)
	categories = models.ForeignKey('Categories', on_delete=models.DO_NOTHING, blank=True, null=True)
	profile_name= models.CharField(max_length=250, null=True, blank=True)
	person_name= models.CharField(max_length=250, null=True, blank=True)
	phone = models.CharField(max_length=15, null=True, blank=True)
	about_us = models.TextField()


	def __str__(self):
		return self.profile_name


class Categories(models.Model):
	name = models.CharField(max_length = 255, blank = True, null = True)
	slug = models.SlugField(max_length=255, blank = True, null = True)

	def __str__(self):
		return self.name 


class ScrapLocations(models.Model):
	city = models.CharField(max_length = 255, blank = True, null = True)

	def __str__(self):
		return self.city 

class ScrapeStatus(models.Model):
	scrape_status = models.BooleanField(blank=True, null=True , default=False)

	def __str__(self):
		return str(self.scrape_status)

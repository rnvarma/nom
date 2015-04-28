from django.db import models
# Create your models here.
class Company(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)
	email = models.CharField(max_length=20)
	website = models.CharField(max_length=50)

class User(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=20)

class FoodEvent(models.Model):
	id = models.AutoField(primary_key=True)
	company = models.ForeignKey(Company)
	name = models.CharField(max_length=50)
	startTime = models.DateTimeField(blank=True)
	endTime = models.DateTimeField(blank=True)
	location = models.CharField(max_length=50)
	description = models.CharField(max_length=100)
	attendees = models.ManyToManyField(User)
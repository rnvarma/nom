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
	orgs = models.ManyToManyField(Company, related_name="admins")

class FoodEvent(models.Model):
	id = models.AutoField(primary_key=True)
	company = models.ForeignKey(Company, related_name="events")
	name = models.CharField(max_length=50)
	date = models.DateField(blank=True, default=None, null=True)
	startTime = models.TimeField(blank=True, default=None, null=True)
	endTime = models.TimeField(blank=True, default=None, null=True)
	location = models.CharField(max_length=50)
	description = models.CharField(max_length=100)
	attendees = models.ManyToManyField(User, related_name="attended_events")

	def __unicode__(self):
		return str(self.date) + " @ " + str(self.startTime)
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Event(models.Model):
	name = models.CharField(max_length=150)
	time = models.CharField(max_length=150)
	lat = models.CharField(max_length=100)
	lng = models.CharField(max_length=100)
	type_of = models.CharField(max_length=100)
	radius = models.CharField(max_length=20)
	description = models.CharField(max_length=300)
	def __str__(self):
		return self.lat

class Citizen(models.Model):
	name = models.CharField(max_length=150)
	age = models.CharField(max_length=100)
	lat = models.CharField(max_length=100)
	lng = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	gender = models.CharField(max_length=10)
	def __str__(self):
		return self.name	

class Center(models.Model):
	name = models.CharField(max_length=100)
	lat = models.CharField(max_length=100)
	lng = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	vicinity = models.CharField(max_length=100)
	place_id = models.CharField(max_length=100)
	types = models.CharField(max_length=100)
	did = models.CharField(max_length=10)
	typeof = models.CharField(max_length=10)
	def __str__(self):
		return self.name

class Message(models.Model):
	number = models.CharField(max_length=100)
	body = models.CharField(max_length=100)
	message_id = models.CharField(max_length=100)
	created = models.CharField(max_length=100)
class Copy(models.Model):
	name = models.CharField(max_length=100)
	lat = models.CharField(max_length=100)
	lng = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	vicinity = models.CharField(max_length=100)
	place_id = models.CharField(max_length=100)
	types = models.CharField(max_length=100)
	did = models.CharField(max_length=10)
	def __str__(self):
		return self.name
class Hospital(models.Model):
	cid = models.CharField(max_length=100)
	current_status = models.CharField(max_length=100)
	capacity = models.CharField(max_length=100)
	def __str__(self):
		return str(self.id)

class Victim(models.Model):
	url = models.CharField(max_length=100)
	name = models.CharField(max_length=150)
	pic_id = models.CharField(max_length=65)
	age = models.CharField(max_length=100)
	gender = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class sms(models.Model):
	number = models.CharField(max_length=100)
	body = models.CharField(max_length=100)
	message_id = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.created)

class Attacker(models.Model):
	ip = models.CharField(max_length=50)

	def __str__(self):
		return self.ip




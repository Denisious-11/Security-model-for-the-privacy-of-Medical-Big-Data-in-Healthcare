from django.db import models

# Create your models here.

class Temp_Users(models.Model):
    u_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    age=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)

class Users(models.Model):
    u_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    age=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)

class Keys(models.Model):
	u_id = models.IntegerField(primary_key=True)
	public_key = models.CharField(max_length=255)
	private_key = models.CharField(max_length=255)

class Images(models.Model):
    image_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255)
    encrypted_image=models.TextField()
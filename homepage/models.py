from django.db import models
from django.contrib.auth.models import User as U

class UserDetails(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

class option(models.Model):
    id = models.AutoField(primary_key=True)
    option = models.CharField(max_length=100)

class Details:
    email : str
    password : str

class Compose:
    recipient : str
    subject : str
    body : str

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    from_message = models.ForeignKey(U, on_delete=models.CASCADE, related_name= "message_from")
    to_message =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_to")
    messsage = models.JSONField()
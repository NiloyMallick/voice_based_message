from django.db import models
from django.contrib.auth.models import User

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



class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "message_from")
    message_to = models.ManyToManyField(User, related_name= "message_to")
    messsage = models.JSONField()


# class UserMessage(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
    # messsage = models.JSONField() 
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
    messsage = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    seen=models.BooleanField(default=False)
    




# class Chat(models.Model):
#     user1=models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user1')
#     user2=models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user2')
#     last_modified=models.DateTimeField(auto_now=True)



# class Message(models.Model):
#     time=models.DateTimeField(auto_now=True)
#     chat=models.ForeignKey(Chat, on_delete=models.CASCADE)
#     sender=models.ForeignKey(User, on_delete=models.CASCADE, related_name='messageSenderUser')
#     receiver=models.ForeignKey(User, on_delete=models.CASCADE, related_name='messageReceiverUser')
#     message=models.CharField(default='', blank=False, null=False, max_length=5000)
#     seen=models.BooleanField(default=False)
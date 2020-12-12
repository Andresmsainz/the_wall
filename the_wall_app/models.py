from django.db import models

# Create your models here.
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        #1 First & Last Name should be at least 2 characters
        if len(postData['firstname']) < 2:
            errors["firstname"] = "First Name should be at least 2 characters!"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "Last Name should be at least 2 characters!"
        #2 email already exists????  
        if len(User.objects.filter(email=postData["email"])) > 0:
            errors["email"] = "This email already exists. Please Pick Another!"
        #3 check that password and confirm password match
        if postData["password"] != postData["confirmpassword"]:
            errors["password"] = "Passwords do not match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wall_Message(models.Model):
    message = models.TextField()
    poster = models.ForeignKey(User,related_name="wall_messages",on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    message = models.TextField()
    poster = models.ForeignKey(User,related_name="wall_comments",on_delete = models.CASCADE)  #connects to user
    wall_message = models.ForeignKey(Wall_Message,related_name="post_comments",on_delete = models.CASCADE)  #connects to wall message
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
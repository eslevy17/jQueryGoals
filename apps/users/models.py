from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Activity(models.Model):
    activity = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Goal(models.Model):
    goal = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="goals")
    created_at = models.DateTimeField(auto_now_add = True)

class Event(models.Model):
    duration = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="events")
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="events", null=True)
    created_at = models.DateField()
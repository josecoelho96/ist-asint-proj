from django.db import models

class User(models.Model):
    ist_id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)
    refresh_token = models.CharField(max_length=30)
    access_token = models.CharField(max_length=30)
    expires_timestamp = models.DateField(max_length=30)

class Room(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(blank=True)
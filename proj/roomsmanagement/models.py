from django.db import models


class User(models.Model):
    ist_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    expires_timestamp = models.DateField()


class Room(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(blank=True)

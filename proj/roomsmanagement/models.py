from django.db import models


class User(models.Model):
    ist_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    # ENHANCEMENT: Photos and stuff


class Space(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    parent_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.id + ':' + self.name


class Room(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    parent_id = models.CharField(max_length=255)

    def __str__(self):
        return self.id + ':' + self.name

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=255)

class Recipient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

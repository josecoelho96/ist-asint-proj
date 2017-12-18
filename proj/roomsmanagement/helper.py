from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, User, Entry
import requests
from django.http import HttpResponse, JsonResponse
from .forms import SearchRoomForm
import datetime

def update_db(request):
    room = Room(id='1111', name='sala1')
    room.save()
    room = Room(id='2222', name='sala2')
    room.save()
    room = Room(id='3333', name='sala3')
    room.save()
    return HttpResponse('done')

    '''response = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")

    rooms = {}
    ids_to_explore = []
    
    for piece in response.json():
        ids_to_explore.append(piece['id'])
    
    for id in ids_to_explore:
        response = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/" + id)
        space = response.json()
        for contained_space in space['containedSpaces']:
            if contained_space['type'] == 'ROOM' and contained_space['name']:
                room = Room(id = contained_space['id'], name = contained_space['name'])
                room.save()
            else:
                ids_to_explore.append(contained_space['id'])'''

def get_room_details(room_id):
    details={}
    try:
        #GET ROOM NAME
        room = Room.objects.get(pk=room_id)
        details['name'] = room.name
        #GET LOGGED USERS IN ROOM
        details['logged_users']= get_logged_users(room_id)
    except Room.DoesNotExist:
        pass
    return details

# CALL IT WHEN YOU WANT TO CHECKIN A USER IN A ROOM
# NOT IMPLEMENTED: REMOVE USER FROM PREVIOUS CHECKED-IN ROOM
def checkin(room_id, user_id):
    try:
        room = Room.objects.get(pk=room_id)
        try:
            user = User.objects.get(pk=user_id)
            entry = Entry(user = user, room = room)
            entry.save()
        except User.DoesNotExist:
            pass
    except Room.DoesNotExist:
        pass

# RETURN ARRAY WITH LOGGED USERS IN ROOM
def get_logged_users(room_id):
    try:
        entries = Entry.objects.exclude(check_out__isnull=False).filter(room=room_id)
        
        logged_users = []
        for entry in entries:
            logged_users.append(entry.user)
        return logged_users
    except Entry.DoesNotExist:
        pass

# CALL IT WHEN YOU WANT TO CHECKOUT A USER IN A ROOM
# NOT IMPLEMENTED: CHECK IF USER EXISTS, CHECK IF ROOM EXISTS, CHECK IN CHECK_OUT IS NULL
def checkout(room_id, user_id):
    try:
        entry = Entry.objects.get(user=user_id, room = room_id)
        entry.check_out = str(datetime.datetime.now())
        entry.save()
    except Entry.DoesNotExist:
        pass
import requests
import json
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count

from roomsmanagement.views import Room, Space, Entry, Recipient, Message


def update_db(request):
    # Delete cached data
    Room.objects.all().delete()
    Space.objects.all().delete()


    BASE_URL = 'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/'
    ids_to_explore = []

    # get campi information
    response = requests.get(BASE_URL).json()    
    for element in response:
        space = Space(id = element['id'], name = element['name'], parent_id = None)
        space.save()
        ids_to_explore.append(element['id'])
    
    # get data from all campi
    for id in ids_to_explore:
        response = requests.get(BASE_URL + id).json()
        # loop on entire list
        for element in response['containedSpaces']:
            # check if it's a room and if the room has a name
            if element['type'] == 'ROOM' and element['name']:
                # the parent is the last id requested
                room = Room(id = element['id'], name = element['name'], parent_id = id)
                room.save()
            elif element['type'] != 'ROOM':
                space = Space(id = element['id'], name = element['name'], parent_id = id)
                space.save()
                ids_to_explore.append(element['id'])

    response = {'success': True, 'message': 'The database was updated sucessfully.'}
    return JsonResponse(response)


def history(request):
    entries = Entry.objects.all()

    data = []
    for entry in entries:
        user = {'id': entry.user.ist_id, 'name': entry.user.name}
        room = {'id': entry.room.id, 'name': entry.room.name}
        check_in = entry.check_in.strftime("%Y-%m-%d %H:%M:%S")
        check_out =  None if not entry.check_out else entry.check_out.strftime("%Y-%m-%d %H:%M:%S")

        data.append({'user': user, 'room': room, 'check-in': check_in, 'check-out': check_out})
        
    response = {'success': True, 'history': data}
    return JsonResponse(response)


def admin_rooms_occupancy(request):

    rooms = []
    # Get all rooms with people inside
    entries = Entry.objects.filter(check_out__isnull=True).values('room').annotate(occupancy=Count('room'))
    
    for entry in entries:
        r = Room.objects.get(pk=entry['room'])
        rooms.append({'id':r.id, 'name':r.name, 'occupancy':entry['occupancy']})
    
    response = {'success': True, 'occupancy': rooms}
    return JsonResponse(response)







def admin_room_details(request, room_id):

    room_details={}

    if room_id:
        try:
            #GET ROOM NAME
            room = Room.objects.get(pk=room_id)
            room_details['name'] = room.name
            room_details['id'] = room_id

            # GET LOGGED USERS IN ROOM
            room_details['logged_users'] = []
            try:
                entries = Entry.objects.exclude(check_out__isnull=False).filter(room=room_id)
                for entry in entries:
                    user = {'id': entry.user.ist_id, 'name': entry.user.name}
                    room_details['logged_users'].append(user)
            except Entry.DoesNotExist:
                return render(request, 'admin/error.html')

            # get all messages to one room
            messages = {}
            recipients=Recipient.objects.filter(room=room)
            for recipient in recipients:
                if recipient.message.id not in messages:
                    msg_details = {'date': recipient.message.timestamp, 'content': recipient.message.content}
                    messages[recipient.message.id] = msg_details
    

        except Room.DoesNotExist:
            response = {'success': False, 'message': 'No room was found.'}
            return JsonResponse(response)
    
    else:
        response = {'success': False, 'message': 'An error happened.'}
        return JsonResponse(response)

    response = {'success': True, 'details': room_details}
    return JsonResponse(response)







def admin_send_message(request):
    return JsonResponse({'result': 'success admin_send_message'})

def admin_get_messages(request):
    return JsonResponse({'result': 'success admin_get_messages'})


def search(request):
    return JsonResponse({'result': 'success search'})

def room_details(request):
    return JsonResponse({'result': 'success room_details'})

def get_messages(request):
    return JsonResponse({'result': 'success get_messages'})

def checkin(request):
    return JsonResponse({'result': 'success checkin'})

def checkout(request):
    return JsonResponse({'result': 'success checkout'})

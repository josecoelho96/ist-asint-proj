import time
import datetime
import os
import requests, json
from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import Room, Space, User, Entry, Message, Recipient
from django.utils.timezone import now
from django.core import serializers


def index(request):
    return render(request, 'roomsmanagement/index.html')

def login(request):
    # TODO: Optimize flow and error checking
    """ Login into fenixedu """

    client_id = os.environ['FENIXEDU_CLIENT_ID']
    redirect_uri = os.environ['FENIXEDU_REDIRECT_URI']

    request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=' + \
        client_id + '&redirect_uri=' + redirect_uri

    return redirect(request_url)


def auth(request):
    # TODO: Optimize flow and error checking
    client_id = os.environ['FENIXEDU_CLIENT_ID']
    redirect_uri = os.environ['FENIXEDU_REDIRECT_URI']
    client_secret = os.environ['FENIXEDU_CLIENT_SECRET']

    # get code provided by fenixedu
    code = request.GET.get('code')

    access_token_request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

    request_data = {'client_id': client_id, 'client_secret': client_secret,
              'redirect_uri': redirect_uri, 'code': code, 'grant_type': 'authorization_code'}

    request_access_token = requests.post(access_token_request_url, data=request_data)

    # check if no errors were raised
    if request_access_token.status_code != 200 or 'error' in request_access_token.json():
        # TODO: Fix this! Make an error page!
        return HttpResponse('An error occured!')
    else:
        access_token = request_access_token.json()['access_token']
        refresh_token = request_access_token.json()['refresh_token']
        token_expires =  request_access_token.json()['expires_in']

        params = {'access_token': access_token}
        request_info = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person', params=params)

        # get user info
        username = request_info.json()['username']
        full_name = request_info.json()['name']

        # save everything into session
        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        request.session['expires'] = token_expires
        request.session['ist_id'] = username
        request.session['full_name'] = full_name
        request.session['checkedin'] = None

        if not User.objects.filter(ist_id=username).exists():
            user = User(ist_id = username, name=full_name)
            user.save()
            
        return redirect( 'roomsmanagement:index' )


def logout(request):
    # TODO: Complete logout flow

    user_id =  request.session.get('ist_id', '')
    checked_in = request.session.get('checkedin', '')
    
    if checked_in:
        try:
            Entry.objects.filter(user=user_id, room = checked_in, check_out__isnull=True).update(check_out = now())
        except Entry.DoesNotExist:
            return render(request, 'roomsmanagement/error.html')

    request.session.flush()
    return redirect('roomsmanagement:index')


def profile(request):
    # TODO: Must be completed or deleted
    return HttpResponse('user details')


def search(request):

    room = request.GET.get('room', '')

    # Look for all rooms that contains the room name inserted before 
    rooms = Room.objects.filter(name__icontains=room)
    rooms_list = {}

    for room in rooms:
        room_info = {}
        parent_spaces = []

        room_info['name'] = room.name
        parent_space_id = room.parent_id
        while parent_space_id != None:
            parent_space = Space.objects.get(id=parent_space_id)
            parent_spaces.insert(0, parent_space.name)
            parent_space_id = parent_space.parent_id

        room_info['parents'] = parent_spaces
        rooms_list[room.id] = room_info
        
    context = {'rooms': rooms_list}
    return render(request, 'roomsmanagement/search.html', context)


def checkin(request):

    room_id = request.POST.get('room', '')
    user_id =  request.session.get('ist_id', '')
    checked_in = request.session.get('checkedin', '')

    if not user_id:
        return redirect( 'roomsmanagement:index' )
    
    if not room_id:
        return render(request, 'roomsmanagement/error.html')


    if room_id == checked_in:
        return redirect('roomsmanagement:room_details')
    
    if checked_in:
        try:
            Entry.objects.filter(user=user_id, room = checked_in, check_out__isnull=True).update(check_out = now())
            request.session['checkedin'] = None
            
        except Entry.DoesNotExist:
            return render(request, 'roomsmanagement/error.html')
        
    try:
        room = Room.objects.get(pk=room_id)
        try:
            user = User.objects.get(pk=user_id)
            entry = Entry(user = user, room = room)
            entry.save()
            request.session['checkedin'] = room_id      
        except User.DoesNotExist:
            return render(request, 'roomsmanagement/error.html')
    except Room.DoesNotExist:
        return render(request, 'roomsmanagement/error.html')
    
    return redirect('roomsmanagement:room_details')
 

def room_details(request):

    room_id = request.session.get('checkedin', '')
    ist_id = request.session.get('ist_id', '')
    if room_id:
        # Checkedin, show details
        details={}
        try:
            #GET ROOM NAME
            room = Room.objects.get(pk=room_id)
            details['name'] = room.name
            details['id'] = room_id

            # GET LOGGED USERS IN ROOM
            details['logged_users'] = []
            try:
                entries = Entry.objects.exclude(check_out__isnull=False).filter(room=room_id)
                for entry in entries:
                    details['logged_users'].append(entry.user.name)
            except Entry.DoesNotExist:
                return render(request, 'roomsmanagement/error.html')
        
        except Room.DoesNotExist:
            return render(request, 'roomsmanagement/error.html')
    else:
        if not ist_id:
            return render(request, 'roomsmanagement/error.html', {'message': 'You must be logged in to view this page!'})
        else:
            return render(request, 'roomsmanagement/error.html', {'message': 'You must be checked-in in a room to view this page!'})


    context = {'room': details}
    return render(request, 'roomsmanagement/room.html', context)


def get_messages(request):
    #IR BUSCAR OS DADOS CERTOS
    room_id = request.session.get('checkedin', '') 
    room = Room.objects.get(pk=room_id)        
    
    user_id = request.session.get('ist_id', '')
    user = User.objects.get(ist_id=user_id) #all messages to user 
    
    recipients=Recipient.objects.filter(user=user, room=room)

    data = []

    for recipient in recipients:
        data.append({'date':recipient.message.timestamp, 'content': recipient.message.content})

    return JsonResponse({'messages':data})
   

# CALL IT WHEN YOU WANT TO CHECKOUT A USER IN A ROOM
def checkout(request):

    room_id = request.session.get('checkedin', '')
    user_id = request.session.get('ist_id', '')

    if room_id:
        # Checkedin, do checkout
        try:
            Entry.objects.filter(user=user_id, room = room_id, check_out__isnull=True).update(check_out = now())
            request.session['checkedin'] = None
        except Entry.DoesNotExist:
            return render(request, 'roomsmanagement/error.html')
        
        return redirect('roomsmanagement:index')
        
    else:
        # no room on session
        if not user_id:
            return render(request, 'roomsmanagement/error.html', {'message': 'You must be logged in to view this page!'})
        else:
            return render(request, 'roomsmanagement/error.html', {'message': 'You must be checked-in in a room to view this page!'})

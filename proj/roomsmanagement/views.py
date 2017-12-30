import time
import os
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Room, Space, User, Entry


def update_db(request):
    # TODO: ERROR CHECKING, LOCK ACCESS, SUITABLE RESPONSE
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

    return HttpResponse('done')


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
        names = full_name.split()
        request.session['display_name'] = ' '.join([names[0], names[-1]])

        return redirect( 'index' )

def logout(request):
    # TODO: Complete logout flow
    request.session.flush()
    return redirect('index')

def profile(request):
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
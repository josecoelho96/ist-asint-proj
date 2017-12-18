import time
import os
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .forms import SearchRoomForm
from .models import Room, User, Entry
from .helper import checkin, get_room_details, checkout


def index(request):

    #update_link = ''

    # context = {'login_url': ''}
    # '''response = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    
    # pre = []

    # for campi in response.json():
    #     pre.append(campi['name'])

    # context = {'campi': pre}'''

    context = {}

    if 'istid' in request.session:
        context['user'] = request.session['istid']
    else:
        context['user'] = None

    return render(request, 'roomsmanagement/index.html', context)


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


def search(request):
    if request.method == 'POST':
        form = SearchRoomForm(request.POST)
        if form.is_valid():
            data = request.POST
            rooms = Room.objects.filter(
                name__icontains=data.__getitem__('room_name'))
            return render(request, 'roomsmanagement/search.html', {'rooms': rooms})

    else:
        form = SearchRoomForm()
    return render(request, 'roomsmanagement/search.html', {'form': form})


def list_rooms(request):
    rooms = Room.objects.all()

    context = {'rooms': rooms}

    return render(request, 'roomsmanagement/listrooms.html', context)


def room_details(request, room_id):

    room = get_room_details(room_id)
    checkout('2222', 'ist181017')
    #return render(request, 'roomsmanagement/roomdetails.html', {'room': room})
    return render(request, 'roomsmanagement/room.html', {'room': room})



def login(request):
    """ Login into fenixedu """

    # Following fenixedu authentication flow
    client_id = os.environ['FENIXEDU_CLIENT_ID']
    redirect_uri = os.environ['FENIXEDU_REDIRECT_URI']

    request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=' + \
        client_id + '&redirect_uri=' + redirect_uri

    return redirect(request_url)


def auth(request):
    """ Login into fenixedu (cont) """

    client_id = os.environ['FENIXEDU_CLIENT_ID']
    redirect_uri = os.environ['FENIXEDU_REDIRECT_URI']
    client_secret = os.environ['FENIXEDU_CLIENT_SECRET']

    # get code provided by fenixedu
    code = request.GET.get('code')

    access_token_request_url = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

    request_data = {'client_id': client_id, 'client_secret': client_secret,
              'redirect_uri': redirect_uri, 'code': code, 'grant_type': 'authorization_code'}

    request_access_token = requests.post(access_token_request_url, data=request_data)

    if 'error' in request_access_token.json():
        # TODO: Fix this! Make an error page!
        return HttpResponse('An error occured!')
    else:
        access_token = request_access_token.json()['access_token']
        refresh_token = request_access_token.json()['refresh_token']
        token_expires =  request_access_token.json()['expires_in']

        params = {'access_token': access_token}
        request_info = requests.get('https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person', params=params)

        # TODO: ERROR CHECK!
        username = request_info.json()['username']
        # save everything into session

        request.session['access_token'] = access_token
        request.session['refresh_token'] = refresh_token
        request.session['expires'] = token_expires
        request.session['istid'] = username

        return redirect( 'index' )

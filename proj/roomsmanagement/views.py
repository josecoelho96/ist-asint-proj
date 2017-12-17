from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, User
import requests
from django.http import HttpResponse, JsonResponse
from .forms import SearchRoomForm
import time

# Create your views here.


def home(request):

    #update_link = ''

    context = {'login_url': ''}
    '''response = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    
    pre = []

    for campi in response.json():
        pre.append(campi['name'])

    context = {'campi': pre}'''

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

    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'roomsmanagement/roomdetails.html', {'room': room})


def login(request):

    CLIENT_ID = '1695915081465897'
    REDIRECT_URI = 'http://localhost:8000/auth'

    REQUEST_URL = 'https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=' + \
        CLIENT_ID + '&redirect_uri=' + REDIRECT_URI

    return redirect(REQUEST_URL)


def auth(request):

    CLIENT_ID = '1695915081465897'
    REDIRECT_URI = 'http://localhost:8000/auth'
    CLIENT_SECRET = '8N9y2/ek6iBQui43OsFVzFfBS1O3H/6x5nRu6mkVEJwqNWs/Qy5DRS35ZEWFyTfutBfpT8mXRnVQ8gnEA06TCA=='
    code = request.GET.get('code')

    REQ_URL = 'https://fenix.tecnico.ulisboa.pt/oauth/access_token'

    PARAMS = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
              'redirect_uri': REDIRECT_URI, 'code': code, 'grant_type': 'authorization_code'}

    r = requests.post(REQ_URL, data=PARAMS)

    ACCESS_TOKEN = r.json()['access_token']
    REFRESH_TOKEN = r.json()['refresh_token']
    EXPIRES_IN = r.json()['expires_in']


# class User(models.Model):
#     ist_id = models.CharField(max_length=30, primary_key=True)
#     name = models.CharField(max_length=30)
#     refresh_token = models.CharField(max_length=30)
#     access_token = models.CharField(max_length=30)
#     expires_timestamp = models.DateField(max_length=30)

    params = {'access_token': ACCESS_TOKEN}

    r = requests.get(
        'https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person', params=params)

    username = r.json()['username']
    name = r.json()['name']

    user = User(ist_id=username, name=name, refresh_token=REFRESH_TOKEN,
                access_token=ACCESS_TOKEN, expires_timestamp=time.strftime("%Y-%m-%d"))

    user.save()

    return HttpResponse(name)

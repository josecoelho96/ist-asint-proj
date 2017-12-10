from django.shortcuts import render
from .models import Room
import requests
from django.http import HttpResponse
from .forms import SearchRoomForm

# Create your views here.

def home(request):

    #update_link = ''
    
    context = {'login_url': ''}
    '''response = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    
    pre = []

    for campi in response.json():
        pre.append(campi['name'])

    context = {'campi': pre}'''

    return render(request, 'roomsmanagement/home.html', context)

def update_db(request):
    room = Room(id = '1111', name = 'sala1')
    room.save()
    room = Room(id = '2222', name = 'sala2')
    room.save()
    room = Room(id = '3333', name = 'sala3')
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

def login(request):
    return HttpResponse('done')

def search(request):
    if request.method == 'POST':
        form = SearchRoomForm(request.POST)
        if form.is_valid():
            data = request.POST
            rooms = Room.objects.filter(name__icontains=data.__getitem__('room_name'))
            return render(request, 'roomsmanagement/search.html', {'rooms': rooms})

    else:
        form = SearchRoomForm()
    return render(request, 'roomsmanagement/search.html', {'form': form})


def list_rooms(request):
    rooms = Room.objects.all()
    
    context = {'rooms': rooms}

    return render(request, 'roomsmanagement/listrooms.html', context)
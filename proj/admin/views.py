import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count

from roomsmanagement.models import Entry, Room, Space


@login_required(login_url='admin:login')
def index(request):

    rooms = []
    # Get all rooms with people inside
    entries = Entry.objects.filter(check_out__isnull=True).values('room').annotate(occupancy=Count('room'))
    
    for entry in entries:
        r = Room.objects.get(pk=entry['room'])

        rooms.append({'id':r.id, 'name':r.name, 'occupancy':entry['occupancy']})
        

    
    context = {'rooms': rooms}
    return render(request, 'admin/index.html', context)


@login_required(login_url='admin:login')
def update_db(request):
    # TODO: ERROR CHECKING, LOCK ACCESS, SUITABLE RESPONSE

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

    context = {'title': 'Update successful', 'message': 'The database was updated sucessfully.'}
    return render(request, 'admin/message.html', context)


@login_required(login_url='admin:login')
def history(request):

    entries = Entry.objects.all()    
    context = {'history': entries}
    return render(request, 'admin/history.html', context=context)


def login_view(request):

    if request.user.is_authenticated:
        return redirect('admin:index')
    else:
        if request.method == 'POST':
            # Try to log user
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            redirect_to = request.POST.get('redirect_to', '')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if redirect_to:
                    return redirect(redirect_to)
                else:
                    return redirect('admin:index')
            else:
                return render(request, 'admin/login.html', {'error': 'Wrong username and/or password! Try again.'})
        else:
            # Display login page
            redirect_to = request.GET.get('next', '')
            return render(request, 'admin/login.html', {'next': redirect_to})


def logout_view(request):

    if request.user.is_authenticated:
        logout(request)
    
    return redirect('admin:index') 


@login_required(login_url='admin:login')
def room_details(request):

    room_id = request.GET.get('room', '')

    details={}

    if room_id:
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
                return render(request, 'admin/error.html')
            
        except Room.DoesNotExist:
            return render(request, 'admin/error.html')

    context = {'room':details}
    return render(request, 'admin/room.html', context)
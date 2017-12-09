from django.shortcuts import render
import requests

# Create your views here.

def home(request):

    response = requests.get("https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces")
    
    pre = []

    for campi in response.json():
        pre.append(campi['name'])

    context = {'campi': pre}
    

    return render(request, 'roomsmanagement/home.html', context)
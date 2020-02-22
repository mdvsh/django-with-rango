from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    abt_link = "Jai Hind Doston ! Go to the" + '<a href="/rango/about"> Rango | About</a>' + ' page .'
    return HttpResponse(abt_link)

def about(request):
    index_link = "Bhau says here is the about page ! Go back to " + '<a href="/rango"> Rango | Home</a>'
    return HttpResponse(index_link)

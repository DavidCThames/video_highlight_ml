from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

def index(request):
        return render(request, "home.html")

def about(request):
        return render(request, "about.html")

def doc(request):
        return render(request, "documentation.html")

def upload(request, positive):
    #get post data
    return render(request, "home.html")

def train(request, positive):
    #get post data
    return render(request, "home.html")

from contextlib import nullcontext
from http.client import HTTPResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from .models import Session, User, Decision, Option

# Create your views here.

def index(request):
    return HttpResponse("Hello this is the home page yes thanks")


def userEntry(request):
    ''' This is the entry point for all users. They enter their name 
    and specify whether they will be creating or joining a session.'''
    return render(request, 'hangapp/userEntry.html')


def startSession(request, session_id):
    '''This is where a user will begin by creating questions and inviting people.'''
    try:
        userId = request.POST['userId']
    except KeyError:
        return HttpResponse("Error: no such user found")
    try:
        user = User.objects.get(pk=userId)
    except:
        # create the new user
        user = User.objects.create("dummy")
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'hangapp/startSession.html', {'session': session, 'user': user})

def vote(request, decision_id):
    # This will be shown to each user to go through all the options to a decision
    decision = get_object_or_404(Decision, pk=decision_id)
    return render(request, 'hangapp/vote.html', {'decision': decision})


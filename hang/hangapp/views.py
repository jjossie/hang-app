from contextlib import nullcontext
from http.client import HTTPResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Session, User, Decision, Option

# Create your views here.

def index(request):
    return HttpResponse("Hello yes this is the home page thanks")


def userEntry(request):
    ''' This is the entry point for all users. They enter their name 
    and specify whether they will be creating or joining a session.'''
    return render(request, 'hangapp/userEntry.html')

def joinSessionNewUser(request):
    print("finna make me a user!")
    try:
        username = request.POST['username']
    except:
        raise Http404(request, "No username for the new User was provided.")
    print(f"his name is {username}")
    newUser = User.objects.create(username=username)
    newUser.save()
    try:
        # Are we joining an existing session?
        sessionId= request.POST['sessionId']
        session = get_object_or_404(Session, pk=sessionId)
    except:
        # No existing sessionID was provided, so we create a new one
        # with the newUser as the creator
        session = Session.objects.create(creator=newUser)
        session.save()
    return render(request, 'hangapp/enterSession.html', {'session': session, 'user': newUser})
    
def joinSessionExistingUser(request, userId):
    user = get_object_or_404(User, pk=userId)
    try:
        # Are we joining an existing session?
        sessionId= request.POST['sessionId']
        session = get_object_or_404(Session, pk=sessionId)
    except:
        raise Http404("Session not found")
    return render(request, 'hangapp/enterSession.html', {'session': session, 'user': user})
    

def addDecision(request, sessionId, userId):
    try:
        text = request.POST['decisionText']
    except:
        raise Http404("Malformed request, missing POST info")

    session = get_object_or_404(Session, pk=sessionId)
    user = get_object_or_404(User, pk=userId)

    # newDecision = Decision.objects.create(decisionText=text, session=session)
    newDecision = session.decision_set.create(decisionText=text)
    newDecision.save()
    return render(request, 'hangapp/enterSession.html', {'session': session, 'user': user})



# def enterSession(request, sessionId, userId):
#     '''This is where a user will begin by creating questions and inviting people.'''
#     # try:
#     #     userId = request.POST['userId']
#     # except KeyError:
#     #     return HttpResponse("Error: no such user found")
#     try:
#         user = User.objects.get(pk=userId)
#     except:
#         # create the new user
#         user = User.objects.create("dummy")
#     session = get_object_or_404(Session, pk=sessionId)
#     return render(request, 'hangapp/enterSession.html', {'session': session, 'user': user})



def voteSession(request, sessionId, userId):
    session = get_object_or_404(Session, pk=sessionId)
    user = get_object_or_404(User, pk=userId)
    decision = session.decision_set.all()[0]
    return render(request, 'hangapp/vote.html', {'decision': decision, 'user': user})

def vote(request, decisionId, userId):
    ''' This will be shown to each user to go through all the options to a decision.
    It is also currently allowing suggestions on the same page so idk bruh
    '''
    decision = get_object_or_404(Decision, pk=decisionId)
    user = get_object_or_404(User, pk=userId)
    try:
        # Check if they are making a new option
        newOptionText = request.POST['optionText']
        print(newOptionText)
        newOption = decision.option_set.create(optionText=newOptionText, author=user)
        # newOption = Option.objects.create(optionText=newOptionText, decision=decision)
        newOption.save()
        print(f"Created new option {newOption}")
    except KeyError:
        # No worries if they didn't POST, that just means they're not making a new option
        print("didn't create a new option")
    except:
        # Something else went wrong, probably database-related
        raise Http404(f"Failed to add option '{newOptionText}'")
    return render(request, 'hangapp/vote.html', {'decision': decision, 'user': user})


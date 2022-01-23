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
    return render(request, 'hangapp/start.html')


def userEntryWithSession(request, sessionId):
    session = get_object_or_404(Session, pk=sessionId)
    return render(request, 'hangapp/start.html', {'session': session})


def newUserJoinSession(request, sessionId):
    try:
        username = request.POST['username']
    except:
        raise Http404(request, "No username for the new User was provided.")
    newUser = User.objects.create(username=username)
    newUser.save()
    session = get_object_or_404(sessionId)
    session.users.add(newUser)
    return render(request, 'hangapp/join.html', {'session': session, 'user': newUser})


def newUserNewSession(request):
    try:
        username = request.POST['username']
    except:
        raise Http404(request, "No username for the new User was provided.")
    newUser = User.objects.create(username=username)
    newUser.save()
    session = Session.objects.create(creator=newUser)
    session.users.add(newUser)
    session.save()
    return render(request, 'hangapp/join.html', {'session': session, 'user': newUser})

# def joinSessionExistingUser(request, userId):
#     user = get_object_or_404(User, pk=userId)
#     try:
#         # Are we joining an existing session?
#         sessionId= request.POST['sessionId']
#         session = get_object_or_404(Session, pk=sessionId)
#     except:
#         raise Http404("Session not found")
#     return render(request, 'hangapp/enterSession.html', {'session': session, 'user': user})


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
    return render(request, 'hangapp/join.html', {'session': session, 'user': user})


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
#     return render(request, 'hangapp/join.html', {'session': session, 'user': user})


def voteSession(request, sessionId, userId):
    session = get_object_or_404(Session, pk=sessionId)
    user = get_object_or_404(User, pk=userId)
    decision = session.decision_set.all()[0]  # change to _set.first()
    return render(request, 'hangapp/suggest.html', {'decision': decision, 'user': user})


def vote(request, optionId, userId):
    ''' Show a user one option at a time and allow them to vote on them
    '''
    option = get_object_or_404(Option, pk=optionId)
    user = get_object_or_404(User, pk=userId)
    
    # Get the vote if one was given
    try:
        voteOnOption = request.POST['vote']

    except:
        print("no vote led into this view")
        return render(request, 'hangapp/vote.html', {'option': option, 'user': user})
        
    # Vote on the option object
    if voteOnOption == 'no':
        option.vote(user, inFavor=False)
    elif voteOnOption == 'yes':
        option.vote(user, inFavor=True)
    else:
        option.vote(user)

    allOptions = option.decision.option_set.all()
    # This might be the most inefficient operation I've ever written
    remainingOptions = list(filter(lambda option:
        not option.usersVoted.contains(user)
    , allOptions))

    print(remainingOptions)

    if len(remainingOptions) == 0:
        # Go to results page
        print("No remaining items, I think")
        for option in allOptions:
            print(f"{option}: \nUsersVoted: {option.usersVoted}")
        # TODO render the results page!!
        return render(request, 'hangapp/results.html', {'decision': option.decision})
    else:
        return render(request, 'hangapp/vote.html', {'option': remainingOptions[0], 'user': user})




def suggest(request, decisionId, userId):
    decision = get_object_or_404(Decision, pk=decisionId)
    user = get_object_or_404(User, pk=userId)
    try:
        # Check if they are making a new option
        newOptionText = request.POST['optionText']
        print(newOptionText)
        newOption = decision.option_set.create(
            optionText=newOptionText, author=user)
        newOption.save()
        print(f"Created new option {newOption}")
    except:
        raise Http404(f"Failed to add option '{newOptionText}'")
    return render(request, 'hangapp/suggest.html', {'decision': decision, 'user': user})



def results(request, decisionId):
    decision = get_object_or_404(Decision, pk=decisionId)
    return render(request, 'hangapp/results.html', {'decision': decision})
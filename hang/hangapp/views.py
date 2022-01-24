from contextlib import nullcontext
from http.client import HTTPResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Session, User, Decision, Option

# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('startUser'))


def userEntry(request):
    ''' This is the entry point for users who will be starting a new
    session.'''
    return render(request, 'hangapp/start.html')


def userEntryWithSession(request, sessionId):
    '''This is the entry point for users who were given a unique session 
    join link.'''
    session = get_object_or_404(Session, pk=sessionId)
    return render(request, 'hangapp/start.html', {'session': session})


def newUserNewSession(request):
    '''New users are directed here after entering their name to be 
    created and saved in the database along with a new session.'''
    try:
        username = request.POST['username']
    except:
        raise Http404(request, "No username for the new User was provided.")
    newUser = User.objects.create(username=username)
    newUser.save()
    session = Session.objects.create(creator=newUser)
    session.joinUser(newUser)
    session.save()
    return render(request, 'hangapp/join.html', {'session': session, 'user': newUser})


def newUserJoinSession(request, sessionId):
    '''Users who are joining an existing session will be directed here
    after entering their name. This is where their name actually gets 
    created.'''
    try:
        username = request.POST['username']
    except:
        raise Http404(request, "No username for the new User was provided.")
    newUser = User.objects.create(username=username)
    newUser.save()
    session = get_object_or_404(Session, pk=sessionId)
    session.joinUser(newUser)
    return render(request, 'hangapp/join.html', {'session': session, 'user': newUser})


def addDecision(request, sessionId, userId):
    '''The join page directs here to create a new Decision to be voted on.'''
    try:
        text = request.POST['decisionText']
    except:
        raise Http404("Malformed request, missing POST info")

    session = get_object_or_404(Session, pk=sessionId)
    user = get_object_or_404(User, pk=userId)

    newDecision = session.decision_set.create(decisionText=text)
    newDecision.save()
    return render(request, 'hangapp/join.html', {'session': session, 'user': user})


def voteSession(request, sessionId, userId):
    '''Once the decisions are set, this view directs the users to start 
    suggesting options for a particular decision. For now all it will only
    allow the first decision to be voted on - all others will be ignored.'''
    session = get_object_or_404(Session, pk=sessionId)
    user = get_object_or_404(User, pk=userId)
    decision = session.decision_set.all()[0]  # change to _set.first()
    return render(request, 'hangapp/suggest.html', {'decision': decision, 'user': user})


def vote(request, optionId, userId):
    '''Show a user one option at a time and allow them to vote on them.
    '''
    option = get_object_or_404(Option, pk=optionId)
    user = get_object_or_404(User, pk=userId)

    # Get the vote if one was given
    try:
        voteOnOption = request.POST['vote']

    except:
        if __debug__:
            print("no vote led into this view")
        return render(request, 'hangapp/vote.html', {'option': option, 'user': user})
    try:
        # Vote on the option object
        if voteOnOption == 'no':
            option.vote(user, inFavor=False)
        elif voteOnOption == 'yes':
            option.vote(user, inFavor=True)
        else:
            option.vote(user)
    except:
        print("Error: This user has already voted.")

    allOptions = option.decision.option_set.all()
    # This might be the most inefficient operation I've ever written
    remainingOptions = list(filter(lambda option:
                                   not option.usersVoted.contains(user), allOptions))
    if __debug__:
        print(remainingOptions)

    if len(remainingOptions) == 0:
        # Go to results page
        return render(request, 'hangapp/results.html', {'decision': option.decision})
    else:
        return render(request, 'hangapp/vote.html', {'option': remainingOptions[0], 'user': user})


def suggest(request, decisionId, userId):
    '''Allow users to create new options for a particular decision.'''
    decision = get_object_or_404(Decision, pk=decisionId)
    user = get_object_or_404(User, pk=userId)
    try:
        # Check if they are making a new option
        newOptionText = request.POST['optionText']
        if __debug__:
            print(newOptionText)
        newOption = decision.option_set.create(
            optionText=newOptionText, author=user)
        newOption.save()
        if __debug__:
            print(f"Created new option {newOption}")
    except:
        raise Http404(f"Failed to add option '{newOptionText}'")
    return render(request, 'hangapp/suggest.html', {'decision': decision, 'user': user})


def results(request, decisionId):
    '''Display the results page for a particular decision.'''
    decision = get_object_or_404(Decision, pk=decisionId)
    return render(request, 'hangapp/results.html', {'decision': decision})

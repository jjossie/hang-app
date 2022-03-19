from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Session, User, Decision, Option

from rest_framework import viewsets, status
from .serializers import OptionSerializer, DecisionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


# REST API Views

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class DecisionViewSet(viewsets.ModelViewSet):
    queryset = Decision.objects.all()
    serializer_class = DecisionSerializer


@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes((permissions.AllowAny,))
def decision_detail(request, pk) -> Response:
    """
    Retrieve, update, or delete a Decision object.
    """
    try:
        decision = Decision.objects.get(pk=pk)
    except Decision.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        # Update an existing decision
        serializer = DecisionSerializer(decision, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        # Get a decision
        serializer = DecisionSerializer(decision)
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == "DELETE":
        # Delete a decision
        decision.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_decision(request) -> Response:
    # TODO fix this, or don't, idk lol
    serializer = DecisionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Vanilla Django Views
# Create your views here.

def index(request):
    return HttpResponseRedirect(reverse('startUser'))


def user_entry(request):
    """ This is the entry point for users who will be starting a new
    session."""
    return render(request, 'hangapp/start.html')


def user_entry_with_session(request, session_id):
    """This is the entry point for users who were given a unique session
    join link."""
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'hangapp/start.html', {'session': session})


def new_user_new_session(request):
    """New users are directed here after entering their name to be
    created and saved in the database along with a new session."""
    try:
        username = request.POST['username']
    except Exception:
        raise Http404(request, "No username for the new User was provided.")
    new_user = User.objects.create(username=username)
    new_user.save()
    session = Session.objects.create(creator=new_user)
    session.join_user(new_user)
    session.save()
    return render(request, 'hangapp/join.html', {'session': session, 'user': new_user})


def new_user_join_session(request, session_id):
    """Users who are joining an existing session will be directed here
    after entering their name. This is where their name actually gets
    created."""
    try:
        username = request.POST['username']
    except Exception:
        raise Http404(request, "No username for the new User was provided.")
    new_user = User.objects.create(username=username)
    new_user.save()
    session = get_object_or_404(Session, pk=session_id)
    session.join_user(new_user)
    return render(request, 'hangapp/join.html', {'session': session, 'user': new_user})


def add_decision(request, session_id, user_id):
    """The join page directs here to create a new Decision to be voted on."""
    try:
        text = request.POST['decisionText']
    except Exception:
        raise Http404("Malformed request, missing POST info")

    session = get_object_or_404(Session, pk=session_id)
    user = get_object_or_404(User, pk=user_id)

    new_decision = session.decision_set.create(decisionText=text)
    new_decision.save()
    return render(request, 'hangapp/join.html', {'session': session, 'user': user})


def vote_session(request, session_id, user_id):
    """Once the decisions are set, this view directs the users to start
    suggesting options for a particular decision. For now all it will only
    allow the first decision to be voted on - all others will be ignored."""
    session = get_object_or_404(Session, pk=session_id)
    user = get_object_or_404(User, pk=user_id)
    decision = session.decision_set.all()[0]  # change to _set.first()
    return render(request, 'hangapp/suggest.html', {'decision': decision, 'user': user})


def vote(request, option_id, user_id):
    """Show a user one option at a time and allow them to vote on them.
    """
    option = get_object_or_404(Option, pk=option_id)
    user = get_object_or_404(User, pk=user_id)

    # Get the vote if one was given
    try:
        vote_on_option = request.POST['vote']

    except Exception:
        if __debug__:
            print("no vote led into this view")
        return render(request, 'hangapp/vote.html', {'option': option, 'user': user})
    try:
        # Vote on the option object
        if vote_on_option == 'no':
            option.vote(user, in_favor=False)
        elif vote_on_option == 'yes':
            option.vote(user, in_favor=True)
        else:
            option.vote(user)
    except Exception:
        print("Error: This user has already voted.")

    all_options = option.decision.option_set.all()
    # This might be the most inefficient operation I've ever written
    remaining_options = list(filter(lambda op:
                                    not op.usersVoted.contains(user), all_options))
    if __debug__:
        print(remaining_options)

    if len(remaining_options) == 0:
        # Go to results page
        return render(request, 'hangapp/results.html', {'decision': option.decision})
    else:
        return render(request, 'hangapp/vote.html', {'option': remaining_options[0], 'user': user})


def suggest(request, decision_id, user_id):
    """Allow users to create new options for a particular decision."""
    decision = get_object_or_404(Decision, pk=decision_id)
    user = get_object_or_404(User, pk=user_id)
    try:
        # Check if they are making a new option
        new_option_text = request.POST['optionText']
        if __debug__:
            print(new_option_text)
        new_option = decision.option_set.create(
            optionText=new_option_text, author=user)
        new_option.save()
        if __debug__:
            print(f"Created new option {new_option}")
    except Exception:
        raise Http404(f"Failed to add option '{new_option_text}'")
    return render(request, 'hangapp/suggest.html', {'decision': decision, 'user': user})


def results(request, decision_id):
    """Display the results page for a particular decision."""
    decision = get_object_or_404(Decision, pk=decision_id)
    return render(request, 'hangapp/results.html', {'decision': decision})

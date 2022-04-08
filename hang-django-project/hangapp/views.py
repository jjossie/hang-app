from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import HangoutSession, Homie, Decision, Option

from rest_framework import viewsets, status
from .serializers import OptionSerializer, DecisionSerializer, VoteDetailSerializer, HangoutSerializer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer

from .custom_config import *
from .utilities import extract_homie


# REST API Views
# *** Class-based

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer

    # This is not working currently, giving 405 errors and idk why
    # @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    # def vote_on_option(self, request, pk=None):
    #     option = self.get_object()
    #     serializer = VoteDetailSerializer(data=request.data)
    #     if serializer.is_valid():
    #         print("Vote Detail serialized successfully")
    #         option.vote("dummy_user", serializer.validated_data['vote'])
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)


class DecisionViewSet(viewsets.ModelViewSet):
    queryset = Decision.objects.all()
    serializer_class = DecisionSerializer


class HangoutViewSet(viewsets.ModelViewSet):
    queryset = HangoutSession.objects.all()
    serializer_class = HangoutSerializer


# *** Function-based
# @csrf_exempt
# @api_view(['POST'])
# def auth_user_entry(request) -> Response:
#     """
#     Given a username in the request, creates a new user (or maybe retrieves the existing one)
#     and logs them into the session.
#     """
#     if request.user.is_authenticated:
#         return Response(data=f"Already Logged In as {request.user.username}", status=status.HTTP_204_NO_CONTENT)
#     try:
#         username = request.data['username']
#         # Check if the user exists
#         user: User = authenticate(request, username=username, password=DEFAULT_GLOBAL_PASSWORD)
#         if user is not None:
#             # Login as the user, which already exists in the database
#             login(request, user)
#             data = {
#                 "username": user.get_username()
#             }
#             return Response(data=data, status=status.HTTP_200_OK)
#         else:
#             # User didn't exist already, so make a new one
#             user = User.objects.create_user(username, password=DEFAULT_GLOBAL_PASSWORD)
#             login(request, user)
#             data = {
#                 "username": user.get_username()
#             }
#             return Response(data=data, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response(e.__str__(), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_join_hangout(request, hangout_id=None) -> Response:
    """
    Two possible entry points: user who has a hangout ID they're trying to join, and one who needs to make one.
    """
    try:
        homie = Homie.get_homie_from_request(request)
    except KeyError as e:
        return Response(data=e.__str__(), status=status.HTTP_400_BAD_REQUEST)
    if hangout_id is None:
        # User did not send a hangout_id, so we'll make one
        hangout = HangoutSession.objects.create(creator=homie)
    else:
        # Get the hangoutSession the user requested to join
        try:
            hangout = HangoutSession.objects.get(pk=hangout_id)
        except ObjectDoesNotExist:
            return Response(data="Invalid Hangout ID", status=status.HTTP_400_BAD_REQUEST)

    hangout.join_homie(homie)
    data = {
        "homieId": homie.pk,
        "hangoutId": hangout.pk
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_view(request) -> Response:
    logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def add_decision(request) -> Response:
    data = request.data
    print(data)
    # I don't think we need the user, but we do need to strip the data
    user = extract_homie(data)
    print(data)
    serializer = DecisionSerializer(data=data)
    if serializer.is_valid():
        print("Decision Data serialized correctly")
        serializer.save()
        return Response(data=data,
                        status=status.HTTP_201_CREATED)
    else:
        # serializer.
        return Response(data=f"Invalid Request body: {request.data}\n\n"
                             f"Errors: {serializer.errors}",
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_decision_for_hangout(request, pk) -> Response:
    # homie = extract_user(request.data)  # Actually I don't think we need this
    hangout = get_object_or_404(HangoutSession, pk=pk)
    # serializer = HangoutSerializer(hangout)
    decision = hangout.decision_set.all()[0]
    serializer = DecisionSerializer(decision)
    response_data = serializer.data
    response_data['decisionId'] = decision.pk
    return Response(
        # data=JSONRenderer().render(serializer.data),
        data=response_data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def get_options_for_decision(request, pk) -> Response:
    decision = get_object_or_404(Decision, pk=pk)
    options = decision.option_set.all()
    response_data = {
        "options": []
    }
    for option in options:
        serializer = OptionSerializer(option)
        response_data["options"].append(serializer.data)
    return Response(
        data=response_data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def add_option(request, decision_pk) -> Response:
    decision = get_object_or_404(Decision, pk=decision_pk)
    user = extract_homie(request.data)
    try:
        option_text = request.data['optionText']
    except KeyError:
        return Response(data={"message": f"request body missing parameter optionText."},
                        status=status.HTTP_400_BAD_REQUEST)
    option = Option.objects.create(
        decision=decision,
        author=user,
        optionText=option_text
    )
    # TODO figure out how to return the option in the response
    # serializer = OptionSerializer(option)
    return Response(
        # data=serializer.data
        data={"message": "successfully created"},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def are_homies_ready(request, hangout_pk):
    hangout = get_object_or_404(HangoutSession, pk=hangout_pk)
    return Response(
        data={"areHomiesReady": hangout.are_homies_ready()},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def ready_up_homie(request):
    user = extract_homie(request.data)
    user.ready_up()
    return Response(data={"message": f"homie {user.username} readied up"},
                    status=status.HTTP_202_ACCEPTED)


# @login_required
@api_view(['POST'])
def vote_on_option(request, pk) -> Response:
    option = get_object_or_404(Option, pk=pk)
    serializer = VoteDetailSerializer(data=request.data)
    if serializer.is_valid():
        print("Vote Detail serialized successfully")
        try:
            # This isn't done until the users stuff is figured out
            homie = extract_homie(request.data)
            print(homie)
            option.vote(homie, serializer.save())
        except Exception as e:
            # TODO implement error messages to the user?
            print(e)
        return Response(data={"vote_tally": option.get_score()},
                        status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# # @permission_classes((permissions.AllowAny,))
# def decision_detail(request, pk) -> Response:
#     """
#     Retrieve, update, or delete a Decision object.
#     """
#     try:
#         decision = Decision.objects.get(pk=pk)
#     except Decision.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "PUT":
#         # Update an existing decision
#         serializer = DecisionSerializer(decision, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
#     elif request.method == "GET":
#         # Get a decision
#         serializer = DecisionSerializer(decision)
#         return Response(serializer.data, status.HTTP_200_OK)
#     elif request.method == "DELETE":
#         # Delete a decision
#         decision.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# Vanilla Django Views
# Create your views here.
#
# def index(request):
#     return HttpResponseRedirect(reverse('startUser'))
#
#
# def user_entry(request):
#     """ This is the entry point for users who will be starting a new
#     session."""
#     return render(request, 'hangapp/start.html')
#
#
# def user_entry_with_session(request, session_id):
#     """This is the entry point for users who were given a unique session
#     join link."""
#     session = get_object_or_404(HangoutSession, pk=session_id)
#     return render(request, 'hangapp/start.html', {'session': session})
#
#
# def new_user_new_session(request):
#     """New users are directed here after entering their name to be
#     created and saved in the database along with a new session."""
#     try:
#         username = request.POST['username']
#     except Exception:
#         raise Http404(request, "No username for the new User was provided.")
#     new_user = Homie.objects.create(username=username)
#     new_user.save()
#     session = HangoutSession.objects.create(creator=new_user)
#     session.join_homie(new_user)
#     session.save()
#     return render(request, 'hangapp/join.html', {'session': session, 'user': new_user})
#
#
# def new_user_join_session(request, session_id):
#     """Users who are joining an existing session will be directed here
#     after entering their name. This is where their name actually gets
#     created."""
#     try:
#         username = request.POST['username']
#     except Exception:
#         raise Http404(request, "No username for the new User was provided.")
#     new_user = Homie.objects.create(username=username)
#     new_user.save()
#     session = get_object_or_404(HangoutSession, pk=session_id)
#     session.join_homie(new_user)
#     return render(request, 'hangapp/join.html', {'session': session, 'user': new_user})
#
#
# def add_decision(request, session_id, user_id):
#     """The join page directs here to create a new Decision to be voted on."""
#     try:
#         text = request.POST['decisionText']
#     except Exception:
#         raise Http404("Malformed request, missing POST info")
#
#     session = get_object_or_404(HangoutSession, pk=session_id)
#     user = get_object_or_404(Homie, pk=user_id)
#
#     new_decision = session.decision_set.create(decisionText=text)
#     new_decision.save()
#     return render(request, 'hangapp/join.html', {'session': session, 'user': user})
#
#
# def vote_session(request, session_id, user_id):
#     """Once the decisions are set, this view directs the users to start
#     suggesting options for a particular decision. For now all it will only
#     allow the first decision to be voted on - all others will be ignored."""
#     session = get_object_or_404(HangoutSession, pk=session_id)
#     user = get_object_or_404(Homie, pk=user_id)
#     decision = session.decision_set.all()[0]  # change to _set.first()
#     return render(request, 'hangapp/suggest.html', {'decision': decision, 'user': user})
#
#
# def vote(request, option_id, user_id):
#     """Show a user one option at a time and allow them to vote on them.
#     """
#     option = get_object_or_404(Option, pk=option_id)
#     user = get_object_or_404(Homie, pk=user_id)
#
#     # Get the vote if one was given
#     try:
#         vote_on_option = request.POST['vote']
#
#     except Exception:
#         if __debug__:
#             print("no vote led into this view")
#         return render(request, 'hangapp/vote.html', {'option': option, 'user': user})
#     try:
#         # Vote on the option object
#         if vote_on_option == 'no':
#             option.vote(user, in_favor=False)
#         elif vote_on_option == 'yes':
#             option.vote(user, in_favor=True)
#         else:
#             option.vote(user)
#     except Exception:
#         print("Error: This user has already voted.")
#
#     all_options = option.decision.option_set.all()
#     # This might be the most inefficient operation I've ever written
#     remaining_options = list(filter(lambda op:
#                                     not op.usersVoted.contains(user), all_options))
#     if __debug__:
#         print(remaining_options)
#
#     if len(remaining_options) == 0:
#         # Go to results page
#         return render(request, 'hangapp/results.html', {'decision': option.decision})
#     else:
#         return render(request, 'hangapp/vote.html', {'option': remaining_options[0], 'user': user})
#
#
# def suggest(request, decision_id, user_id):
#     """Allow users to create new options for a particular decision."""
#     decision = get_object_or_404(Decision, pk=decision_id)
#     user = get_object_or_404(Homie, pk=user_id)
#     try:
#         # Check if they are making a new option
#         new_option_text = request.POST['optionText']
#         if __debug__:
#             print(new_option_text)
#         new_option = decision.option_set.create(
#             optionText=new_option_text, author=user)
#         new_option.save()
#         if __debug__:
#             print(f"Created new option {new_option}")
#     except Exception:
#         raise Http404(f"Failed to add option '{new_option_text}'")
#     return render(request, 'hangapp/suggest.html', {'decision': decision, 'user': user})
#
#
# def results(request, decision_id):
#     """Display the results page for a particular decision."""
#     decision = get_object_or_404(Decision, pk=decision_id)
#     return render(request, 'hangapp/results.html', {'decision': decision})

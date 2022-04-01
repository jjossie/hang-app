from enum import Enum

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

class Vote(Enum):
    NO = 0
    NEUTRAL = 1
    YES = 2


class VoteDetail:
    def __init__(self, vote: int, time_passed: float):
        self.vote = Vote(vote)  # Ensure the int is either 0, 1, or 2
        self.time_passed = time_passed


class Option(models.Model):
    """Represents an option to vote on for a particular decision."""

    _authorBiasFactor = 0.8

    optionText = models.CharField(max_length=400)
    score = models.FloatField(default=0.0)
    author = models.ForeignKey(
        "hangapp.Homie", on_delete=models.CASCADE, related_name="author")
    decision = models.ForeignKey("Decision", on_delete=models.CASCADE)
    usersVoted = models.ManyToManyField("hangapp.Homie")

    def __str__(self):
        return f"Option: {self.optionText} with score {self.score}"

    def vote(self, user, vote_detail: VoteDetail):
        """The given user votes on this choice. Yes if inFavor is True,
        no if it is False, or neutral if undefined."""
        if self.usersVoted.all().contains(user):
            raise Exception('User has already voted')

        if vote_detail.vote == Vote.YES:
            vote_weight = 1
        elif vote_detail.vote == Vote.NO:
            vote_weight = -1
        else:
            assert(vote_detail.vote == Vote.NEUTRAL)
            vote_weight = 0

        # TODO do something with the time_passed param
        if user == self.author:
            vote_weight *= Option._authorBiasFactor
        self.usersVoted.add(user)
        self.score += vote_weight
        self.save()

    def get_score(self):
        return self.score

    def voting_finished(self):
        users_in_session = self.decision.session.users.all()
        print(f"Session: {users_in_session}")
        print(f"This Option: {self.usersVoted.all()}")
        return set(users_in_session) == set(self.usersVoted.all())


class Decision(models.Model):
    """Represents a decision that a group of friends is making."""

    decisionText = models.CharField(max_length=400)
    session = models.ForeignKey("hangapp.HangoutSession", on_delete=models.CASCADE)

    def __str__(self):
        return f"Decision: {self.decisionText}"

    def add_option(self, option):
        self.options.append(option)
        option.setParentDecision(self)

    def get_winner(self):
        options = self.option_set.all()
        winner = options[0]
        for option in options:
            score = option.get_score()
            if score > winner.get_score():
                winner = option
        return winner

    def voting_finished(self) -> bool:
        for option in self.option_set.all():
            if not option.voting_finished():
                return False
        return True


class Homie(models.Model):
    """Represents a single user of the web app. Currently, only used
    to identify who made a particular decision or option."""

    username = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.username

    pass


class HangoutSession(models.Model):
    """Represents a session of decision-making by a group of friends."""

    creator = models.ForeignKey(
        Homie, on_delete=models.CASCADE, related_name="creator")
    users = models.ManyToManyField(Homie)

    def __str__(self):
        return f"Session created by {self.creator}"

    def join_user(self, user):
        self.users.add(user)
        print(f"Just added user {user.username} to session {self.id}")
        print(self.users.all())

    def get_invite_link(self):
        return reverse('startUserWithSession', args=(self.id,))

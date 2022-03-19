from django.db import models
from django.urls import reverse

# Create your models here.


class Option(models.Model):
    """Represents an option to vote on for a particular decision."""

    _authorBiasFactor = 0.8

    optionText = models.CharField(max_length=400)
    score = models.FloatField(default=0.0)
    author = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="author")
    decision = models.ForeignKey("Decision", on_delete=models.CASCADE)
    usersVoted = models.ManyToManyField("User")

    def __str__(self):
        return f"Option: {self.optionText} with score {self.score}"

    def vote(self, user, in_favor=None):
        """The given user votes on this choice. Yes if inFavor is True,
        no if it is False, or neutral if undefined."""
        if self.usersVoted.all().contains(user):
            raise Exception('User has already voted')

        if in_favor is None:
            vote_weight = 0
        else:
            vote_weight = 1 if in_favor else -1
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
    session = models.ForeignKey("Session", on_delete=models.CASCADE)

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


class User(models.Model):
    """Represents a single user of the web app. Currently, only used
    to identify who made a particular decision or option."""

    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    pass


class Session(models.Model):
    """Represents a session of decision-making by a group of friends."""

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"Session created by {self.creator}"

    def join_user(self, user):
        self.users.add(user)
        print(f"Just added user {user.username} to session {self.id}")
        print(self.users.all())

    def get_invite_link(self):
        return reverse('startUserWithSession', args=(self.id,))

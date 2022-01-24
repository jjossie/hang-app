from django.db import models
from django.urls import reverse

# Create your models here.


class Option(models.Model):
    '''Represents an option to vote on for a particular decision.'''

    _authorBiasFactor = 0.8

    optionText = models.CharField(max_length=400)
    score = models.FloatField(default=0.0)
    author = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="author")
    decision = models.ForeignKey("Decision", on_delete=models.CASCADE)
    usersVoted = models.ManyToManyField("User")

    def __str__(self):
        return f"Option: {self.optionText} with score {self.score}"

    def vote(self, user, inFavor=None):
        '''The given user votes on this choice. Yes if inFavor is True, 
        no if it is False, or neutral if undefined.'''
        if self.usersVoted.all().contains(user):
            raise Exception('User has already voted')

        if inFavor is None:
            voteWeight = 0
        else:
            voteWeight = 1 if inFavor else -1
        if (user == self.author):
            voteWeight *= Option._authorBiasFactor
        self.usersVoted.add(user)
        self.score += voteWeight
        self.save()

    def getScore(self):
        return self.score

    def votingFinished(self):
        usersInSession = self.decision.session.users.all()
        print(f"Session: {usersInSession}")
        print(f"This Option: {self.usersVoted.all()}")
        return set(usersInSession) == set(self.usersVoted.all())


class Decision(models.Model):
    '''Represents a decision that a group of friends is making.'''

    decisionText = models.CharField(max_length=400)
    session = models.ForeignKey("Session", on_delete=models.CASCADE)

    def __str__(self):
        return f"Decision: {self.decisionText}"

    def addOption(self, option):
        self.options.append(option)
        option.setParentDecision(self)

    def getWinner(self):
        options = self.option_set.all()
        winner = options[0]
        for option in options:
            score = option.getScore()
            if score > winner.getScore():
                winner = option
        return winner

    def votingFinished(self) -> bool:
        for option in self.option_set.all():
            if not option.votingFinished():
                return False
        return True


class User(models.Model):
    '''Represents a single user of the web app. Currently only used 
    to identify who made a particular decision or option.'''

    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    pass


class Session(models.Model):
    '''Represents a session of decision-making by a group of friends.'''

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="creator")
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"Session created by {self.creator}"

    def joinUser(self, user):
        self.users.add(user)
        print(f"Just added user {user.username} to session {self.id}")
        print(self.users.all())

    def getInviteLink(self):
        return reverse('startUserWithSession', args=(self.id,))

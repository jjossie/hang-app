from django.db import models

class Option(models.Model):

    _authorBiasFactor = 0.8

    def __init__(self, name, author) -> None:
        self.name = name
        self.score = 0 
        self.votes = []
        self.score = 0
        self.author = author
    
    def __str__(self):
        return f"Option: {self.name} with score {self.score}"

    def setParentDecision(self, parent):
        self.parentDecision = parent

    def getParentDecision(self):
        return self.parentDecision

    def _vote(self, user, value):
        # check to see if this user has voted already and raise an error if so
        self.votes.append((user, value))
        self.score += value

    def voteYes(self, user):
        if user == self.author:
            self._vote(user, 1 * Option._authorBiasFactor)
        else:
            self._vote(user, 1)

    def voteNo(self, user):
        if user == self.author:
            self._vote(user, -1 * Option._authorBiasFactor)
        else:
            self._vote(user, -1)

    def voteNeutral(self, user):
        self._vote(user, 0)
    
    def getScore(self):
        sum = 0
        for vote in self.votes:
            sum += vote[1]
        assert sum == self.score
        return self.score

    def votingFinished(self):
        users = set(self.parentDecision.getParentSession().getUsers())
        # for user in users:
        usersVoted = set()
        for vote in self.votes:
            usersVoted.add(vote[0])
        

        print(users)
        print(usersVoted)
        return usersVoted == users

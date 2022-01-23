from django.db import models
from django.urls import reverse
# Create your models here.


class Option(models.Model):

    _authorBiasFactor = 0.8

    optionText = models.CharField(max_length=400)
    score = models.FloatField(default=0.0)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    # usersVoted = models.ForeignKey("User", on_delete=models.CASCADE, null=True) # TODO figure this out
    decision = models.ForeignKey("Decision", on_delete=models.CASCADE)
    usersVoted = models.ManyToManyField("User")

    def __str__(self):
        return f"Option: {self.optionText} with score {self.score}"

    def vote(self, user, inFavor=None):
        '''The given user votes on this choice. Yes if inFavor is True, 
        no if it is False, or neutral if undefined.'''
        if inFavor is None:
            voteWeight = 0
        else:
            voteWeight = 1 if inFavor else -1 
        if (user == self.author): # make sure this equality operator works
            voteWeight *= Option._authorBiasFactor
        # TODO check to see if this user has voted already and raise an error if so
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

    decisionText = models.CharField(max_length=400)
    session = models.ForeignKey("Session", on_delete=models.CASCADE)

    def __str__(self):
        return f"Decision: {self.decisionText}"


    ''' TODO Fix all of these functions'''

    def addOption(self, option):
        self.options.append(option)
        option.setParentDecision(self)

    def getOptions(self):
        return self.options

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

    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    pass


class Session(models.Model):

    # users = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # decisions = models.ForeignKey(Decision, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"Session created by {self.creator}"

    def joinUser(self, user):
        self.users.add(user)

    def getInviteLink(self):
        return reverse('newUserJoinSession', args=(self.id,))



# def main_test():

#     u1 = User("Tony")
#     u2 = User("Steve")
#     u3 = User("Peter")
#     u4 = User("Bruce")

#     session = Session(u1)
#     session.joinUser(u1)
#     session.joinUser(u2)

#     o1 = Option("Taco Bell", u1)
#     o2 = Option("McDonald's", u2)
#     o3 = Option("The Hickory", u1)
#     o4 = Option("Wendy's", u1)

#     question = Decision("Where should we eat?")
#     session.addDecision(question)

#     question.addOption(o1)
#     question.addOption(o2)
#     question.addOption(o3)
#     question.addOption(o4)

#     print("Pre-voting: ")

#     for option in question.getOptions():
#         print(option)

#     o1.voteYes(u1)
#     o1.voteYes(u2)
#     o1.voteNo(u3)
#     o1.voteNeutral(u4)

#     o2.voteNeutral(u1)
#     o2.voteNo(u2)
#     o2.voteNo(u3)
#     o2.voteNo(u4)

#     o3.voteNo(u1)
#     o3.voteYes(u2)
#     o3.voteNeutral(u3)
#     o3.voteYes(u4)

#     o4.voteYes(u1)
#     o4.voteNo(u2)
#     o4.voteNo(u3)
#     o4.voteNo(u4)

#     # print("\n\nPost-voting: ")
#     # for option in question.getOptions():
#     #     print(option)
#     # print("\n\nWinner:")
#     # print(question.getWinner())

#     print(o1.votingFinished())

# if __name__ == '__main__':
#     main_test()

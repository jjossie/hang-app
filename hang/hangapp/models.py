from mimetypes import init
from django.db import models

# Create your models here.


class Session():

    lastId = 1

    def __init__(self, creator) -> None:
        self.userlist = []
        self.decisionlist = []
        self.creator = creator

    def __str__(self):
        return f"Session created by {self.creator}"

    def joinUser(self, user):
        self.userlist.append(user)

    def addDecision(self, decision):
        self.decisionlist.append(decision)
        decision.setParentSession(self)

    def getUsers(self):
        return self.userlist

    def generateID(self) -> int:
        Session.lastId += 1
        val = hash(Session.lastId)
        print(val)
        return val

    

class User:
    
    def __init__(self) -> None:
        self.name = ""
        
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self):
        return self.name

class Decision:

    def __init__(self) -> None:
        self.prompt = ""

    def __init__(self, prompt) -> None:
        self.prompt = prompt
        self.options = []

    def __str__(self):
        return self.prompt

    def setParentSession(self, parent):
        self.parentSession = parent

    def getParentSession(self):
        return self.parentSession

    def addOption(self, option):
        self.options.append(option)
        option.setParentDecision(self)

    def getOptions(self):
        return self.options

    def getWinner(self):
        winner = self.options[0]
        for option in self.options:
            score = option.getScore()
            if score > winner.getScore():
                winner = option

        return winner

    def isFinished(self) -> bool:
        for option in self.options:
            if not option.votingComplete():
                return False
        
        return True


class Option:

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
        

def main_test():


    u1 = User("Tony")
    u2 = User("Steve")
    u3 = User("Peter")
    u4 = User("Bruce")

    session = Session(u1)
    session.joinUser(u1)
    session.joinUser(u2)
    print(session.generateID())

    o1 = Option("Taco Bell", u1)
    o2 = Option("McDonald's", u2)
    o3 = Option("The Hickory", u1)
    o4 = Option("Wendy's", u1)
    


    question = Decision("Where should we eat?")
    session.addDecision(question)

    question.addOption(o1)
    question.addOption(o2)
    question.addOption(o3)
    question.addOption(o4)

    print("Pre-voting: ")

    for option in question.getOptions():
        print(option)

    o1.voteYes(u1)
    o1.voteYes(u2)
    o1.voteNo(u3)
    o1.voteNeutral(u4)

    o2.voteNeutral(u1)
    o2.voteNo(u2)
    o2.voteNo(u3)
    o2.voteNo(u4)

    o3.voteNo(u1)
    o3.voteYes(u2)
    o3.voteNeutral(u3)
    o3.voteYes(u4)
    
    o4.voteYes(u1)
    o4.voteNo(u2)
    o4.voteNo(u3)
    o4.voteNo(u4)

    # print("\n\nPost-voting: ")
    # for option in question.getOptions():
    #     print(option)
    # print("\n\nWinner:")
    # print(question.getWinner())

    print(o1.votingFinished())



if __name__ == '__main__':
    main_test()
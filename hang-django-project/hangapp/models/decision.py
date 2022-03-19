from django.db import models

class Decision(models.Model):

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
            score = option.get_score()
            if score > winner.get_score():
                winner = option

        return winner

    def isFinished(self) -> bool:
        for option in self.options:
            if not option.votingComplete():
                return False
        
        return True

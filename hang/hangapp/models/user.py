from django.db import models

class User(models.Model):
    
    username = models.CharField(max_length=100)

    def __init__(self) -> None:
        self.username = ""
        
    def __init__(self, username) -> None:
        self.username = username

    def __str__(self):
        return self.username

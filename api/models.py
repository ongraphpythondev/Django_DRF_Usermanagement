from django.db import models

# Create your models here.

class UserData(models.Model):
    email = models.EmailField(max_length=254)
    username = models.CharField( max_length=50)
    # lastname = models.CharField( max_length=50)
    password = models.CharField( max_length=50)
    
    def __str__(self):
        return self.username
    

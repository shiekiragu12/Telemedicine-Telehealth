from django.db import models

# Create your models here.


class Media(models.Model):
    file = models.ImageField(upload_to='images/uploaded/')

    created_on = models.DateTimeField(auto_created=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True, auto_now=True)


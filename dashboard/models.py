from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=6, null=True)
    contact_number = models.IntegerField(null=True)
    address = models.CharField(max_length=100, null=True)
    birthdate = models.CharField(max_length=50, null=True)
    about = models.TextField(null=True)
    profile_pic = models.ImageField(default='images/default.png', upload_to='images')

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "notes"

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


from threading import Lock
import os
import json
import re
from .utils import _read_config_file, _diff 

class Document(models.Model):
    docfile = models.CharField(null=False, max_length=255)
    finished = models.BooleanField(null=False, default=False)
    score = models.IntegerField(null=False, default=0)
    stdout = models.CharField(null=False, default = '', max_length=1000)
    stderr = models.CharField(null=False, default = '', max_length=100000)
    score = models.FloatField(null=False, default=0.0)
    test_value = models.FloatField(null=False, default=0.0)
    tests_result = models.CharField(null=False, default='', max_length=1000)
    tests_time = models.CharField(null=False, default='', max_length=1000)
    date = models.DateTimeField(null=False, auto_now_add=True)
    problemobj = models.ForeignKey('Problem', default='', on_delete=models.CASCADE)

class Problem(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    number = models.IntegerField(null=False)
    name = models.CharField(null=False, default='', max_length=100)
    coins_awarded = models.IntegerField(null=False, default=0)
    text = models.CharField(null=False, default='', max_length=10000)
    examples = models.CharField(null=False, default = '', max_length=100000)
    difficulty = models.IntegerField(null=False, default = 0)
    time_limit = models.FloatField(null=False, default = 0.0)
    memory_limit = models.IntegerField(null=False, default = 0)
    source_limit = models.IntegerField(null=False, default = 0) 
    sources = models.ManyToManyField(to='checker.Document')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    problems = models.ManyToManyField(to='checker.Problem')
    sources = models.ManyToManyField(to='checker.Document')
    coins = models.IntegerField(null=False, default=0)
    image = ProcessedImageField(upload_to='img', null=True, default='placeholder.png', processors=[ResizeToFill(200,200)])

class Handler():
    __instance = None

    @staticmethod
    def get_instance():
        if Handler.__instance is None:
            Handler()
        return Handler.__instance

    def __init__(self):
        if Handler.__instance is not None:
            raise Exception("Multiple Lock Handlers created")
        else:
            Handler.__instance = self

        self.__mutex = Lock()

    def acquire_mutex(self):
        print("mutex acquired")
        self.__mutex.acquire()
    
    def release_mutex(self):
        print("mutex released")
        self.__mutex.release()

 
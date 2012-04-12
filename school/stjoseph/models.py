from django.db import models
import Image
# Create your models here.

class sjcuser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    tit = models.CharField(max_length=2)
    cla = models.CharField(max_length=2, null=True, blank=True)
    yj = models.CharField(max_length=5, null=True, blank=True)
    yop = models.CharField(max_length=5, null=True, blank=True)
    subj = models.TextField(null=True, blank=True)
    cw = models.TextField()
    lf = models.URLField(null=True, blank=True)
    con = models.CharField(max_length=20, null=True, blank=True)
    act = models.BooleanField(default=False)
    actn = models.TextField(null=True, blank=True)
    
class presrqst(models.Model):
    uid = models.IntegerField(primary_key=True)
    actn = models.TextField(null=True, blank=True)

class schoolim(models.Model):
    name = models.CharField(max_length=20)
    albname = models.CharField(max_length=20)
    vistoall = models.BooleanField()

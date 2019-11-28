from django.db import models
from django.utils.timezone import now

class User(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    dob = models.DateTimeField(default=now)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    bankNo = models.IntegerField(default=0)
    phoneNo = models.IntegerField(default=0)
    profileCreated = models.DateTimeField('date created')

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    condition = models.CharField(max_length=200)
    image = models.ImageField(upload_to='item_pictures', blank=True, default='item_pictures/default.png')
    useritem = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

class Auction(models.Model):
    starts = models.DateTimeField('start date')
    ends = models.DateTimeField('end date')
    auctionitem = models.OneToOneField(Item, on_delete=models.CASCADE)

class Bid(models.Model):
    belongstoauction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    belongstouser = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

class Question(models.Model):
    aboutAuction = models.IntegerField(default=0)
    fromUser = models.IntegerField(default=0)
    toUser = models.IntegerField(default=0)
    message = models.CharField(max_length=200, default=None)
    response = models.CharField(max_length=200, default=None)
    answered = models.BooleanField(default = False)

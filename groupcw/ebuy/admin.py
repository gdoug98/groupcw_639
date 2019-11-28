
from django.contrib import admin

from .models import User, Item, Auction, Bid, Question

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Question)

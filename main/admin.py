from django.contrib import admin
from .models import requests, platforms, review, address

admin.site.register(requests)
admin.site.register(platforms)
admin.site.register(review)
admin.site.register(address)
"""Admin python file """
from django.contrib import admin
from .models import User, Admin, Event, Book_ground
"""Configuration class for the SCMApp application """
# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Event)
admin.site.register(Book_ground)

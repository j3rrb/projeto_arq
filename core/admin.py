from django.contrib import admin
from .models import Group, Location, Product, Manufacturer, Sale

admin.site.register([Group, Location, Product, Manufacturer, Sale])

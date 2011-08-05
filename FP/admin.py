#!/usr/bin/python
from FP.models import *
from django.contrib import admin

class MyAdmin(admin.ModelAdmin):
    pass

admin.site.register(feedDB )
admin.site.register(itemDB)
#!/usr/bin/python
from FP.models import *
from django.contrib import admin

class MyAdmin(admin.ModelAdmin):
    pass

admin.site.register(feedDB , MyAdmin)
admin.site.register(itemDB)
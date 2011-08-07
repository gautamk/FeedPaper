#!/usr/bin/python
from FeedPaper.FP.models import feedDB ,itemDB
from django.contrib import admin



class itemDBAdmin(admin.ModelAdmin):
    readonly_fields = ('feed' , 'title' , 'description' , 'link_url' , 'checksum' , )
    list_display = ('title' ,  'link_url' , 'description'  )
    list_display_links = ('title' ,  'description'  )
    fieldsets = (
        (None, {
            'fields': ('feed', 'title', 'description' , 'link_url' ,)
        }),
        ('Advanced details', {
            'classes': ('collapse',),
            'fields': ('checksum',)
        }),
    )
class itemDBAdminInLine(admin.StackedInline):
    model = itemDB
    readonly_fields = ('feed' , 'title' , 'description' , 'link_url' , 'checksum' , )
    extra = 0
 
class feedDBAdmin(admin.ModelAdmin):
    readonly_fields = ('checksum',)
    list_display_links = ('keyword',)
    list_editable = ( 'url',)
    list_display = ('keyword', 'url',)
    inlines = [itemDBAdminInLine]
    fieldsets = (
        (None, {
            'fields': ('keyword', 'url',)
        }),
        ('Advanced details', {
            'classes': ('collapse',),
            'fields': ('checksum',)
        }),
    )
   
admin.site.register(feedDB  ,feedDBAdmin )
admin.site.register(itemDB , itemDBAdmin)
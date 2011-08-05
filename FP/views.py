# Create your views here
from FeedPaper.FP.models import *
from django.http import HttpResponse ,HttpResponseRedirect
import feedparser
from django.template import loader , Context

def UpdateItems(request):
    feeds = feedDB.objects.all()
    for feed in feeds:
        parse = feedparser.parse(feed.url)
        for entry in parse['entries']:
            itemDB(
                   title =  entry.title,
                   description = entry.summary,
                   link_url = entry.link ,
                   feed = feed,
                   ).save()
    
    return HttpResponseRedirect('/admin')

def ShowUpdateItems(request):
    output=""
    feeds = feedDB.objects.all()
    for feed in feeds:
        parse = feedparser.parse(feed.url)
        output +="""
        
        <h1>%s</h1>
        <h2><a href="%s" target="_blank">Feed Link</a></h2>
        """ %(feed.keyword , feed.url)
        for entry in parse['entries']:
            output += """
            <style>
            div
            {
                border: 3px ridge;
                margin:15px;
            }
            </style>
            <div>
            Title : <p><a href="%s" target="_blank"> %s </a></p>
            Summary : <p> %s </p>
            
            </div>
            """%(entry.link  , entry.title , entry.summary , )
    
    return HttpResponse(output)
    
    # HTML Content
    # fd['entries'][0].content[0].value
    # Description
    # fd['entries'][0].summary


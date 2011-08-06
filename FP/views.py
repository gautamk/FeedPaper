# Create your views here
import feedparser

from django.db import IntegrityError
from FeedPaper.FP.models import *
from django.http import HttpResponse ,HttpResponseRedirect
from django.template import loader , Context
from django.shortcuts import render_to_response




def CSVUploadView(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            from FeedPaper.FP.controllers import parseCSV
            parseCSV(request.FILES['file'])
            return HttpResponseRedirect('/admin')
        else:
            form = CSVUploadForm()
        return render_to_response('upload.html', {'form': form , 
                                                  'error' : 'Unable to Process File / Invalid File',})

def UpdateItems(request):
    from FeedPaper.FP.controllers import calculate_checksum
    feeds = feedDB.objects.all()
    for feed in feeds:
        parse = feedparser.parse(feed.url)
        for entry in parse['entries']:
            
            try: 
                itemDB(
                       title =  entry.title,
                       description = entry.summary,
                       link_url = entry.link ,
                       feed = feed,
                       ).save()
            except IntegrityError:
                pass
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
            str = entry.title + entry.summary + entry.link
            str = str.encode('ascii' , 'xmlcharrefreplace')
            hash = hashlib.sha1(str).hexdigest().encode('utf-8')
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
            Hash: <p> %s </p>
            </div>
            """%(entry.link  , entry.title , entry.summary , hash )
    
    return HttpResponse(output)
    
    # HTML Content
    # fd['entries'][0].content[0].value
    # Description
    # fd['entries'][0].summary


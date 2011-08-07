# Create your views here
import feedparser

from django.db import IntegrityError
from FeedPaper.FP.models import feedDB , itemDB , CSVUploadForm
from django.http import HttpResponse , HttpResponseRedirect
# from django.template import loader , Context
from django.shortcuts import render_to_response
from FeedPaper.FP.controllers import calculate_checksum



def CSVUploadView(request):
    from django.core.context_processors import csrf
    form = CSVUploadForm(request.POST, request.FILES)
    c = {'form':form,'error':"",}
    c.update(csrf(request))
    if request.method == "GET":
        
        return render_to_response('upload.html', c )    
    if request.method == "POST":
        if form.is_valid():
            from FeedPaper.FP.controllers import parseCSV
            parseCSV(request.FILES['file'])
            return HttpResponseRedirect('/admin')
        else:
            form = CSVUploadForm()
            c['error'] = "Error in Uploading File / Invalid Format"
        return render_to_response('upload.html', c )

def UpdateItems(request):
    
    feeds = feedDB.objects.all()
    for feed in feeds:
        parse = feedparser.parse(feed.url)
        for entry in parse['entries']:
            
            try: 
                itemDB(
                       title=entry.title,
                       description=entry.summary,
                       link_url=entry.link ,
                       feed=feed,
                       ).save()
            except IntegrityError:
                pass
    return HttpResponseRedirect('/admin')

def ShowUpdateItems(request):
    output = ""
    feeds = feedDB.objects.all()
    for feed in feeds:
        parse = feedparser.parse(feed.url)
        output += """
        
        <h1>%s</h1>
        <h2><a href="%s" target="_blank">Feed Link</a></h2>
        """ % (feed.keyword , feed.url)
        for entry in parse['entries']:
            hash = calculate_checksum(entry.title + entry.summary + entry.link)
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
            """ % (entry.link  , entry.title , entry.summary , hash)
    
    return HttpResponse(output)
    



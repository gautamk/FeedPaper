# Create your views here
import feedparser

from django.db import IntegrityError
from FeedPaper.FP.models import feedDB , itemDB , CSVUploadForm
from django.http import HttpResponse , HttpResponseRedirect
# from django.template import loader , Context
from django.shortcuts import render_to_response
from FeedPaper.FP.controllers import calculate_checksum
import re, htmlentitydefs

##
# Removes HTML or XML character references and entities from a text string.
# From : http://effbot.org/zone/re-sub.htm#unescape-html
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def LandingPage(request):
    if request.method == "GET":
        template_values={
                         'keywords':feedDB.objects.all(),
                         }
        try:
            if request.GET['keyword'] != '' :
                fdb = feedDB.objects.all().filter(keyword = request.GET['keyword'] )
                template_values={
                                 'keywords':feedDB.objects.all(),
                                 'posts':itemDB.objects.all().filter(feed = fdb),
                                 }
                return render_to_response('landing_page.html',template_values)
        except KeyError:
            return render_to_response('landing_page.html',template_values)

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
                       description= unescape( entry.summary ),
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
    



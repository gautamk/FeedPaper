from django.db import models
from django import forms


# Create your models here.
class feedDB(models.Model):
    keyword = models.CharField(max_length = 200)
    url = models.URLField()
    time_stamp = models.DateTimeField(auto_now = True)
    checksum = models.CharField(max_length = 200 , unique = True )
    
    def save(self):
        from FeedPaper.FP.controllers import calculate_checksum
        self.checksum = calculate_checksum(self.keyword + self.url )
        super(feedDB , self).save()
       
    
#    def create_checksum(self,sender,instance,created):
#        from FeedPaper.FP.controllers import calculate_checksum
#        if created:
#            self.checksum = calculate_checksum(self.keyword + self.url)   
#            print self.checksum  
    def __unicode__(self):
        return self.keyword
    
class itemDB(models.Model):
    feed = models.ForeignKey('feedDB')
    title = models.CharField(max_length = 200)
    description = models.TextField()
    link_url = models.URLField()
    time_stamp = models.DateTimeField(auto_now = True)
    
    # Check sum is used to prevent duplication of entries 
    checksum = models.CharField(max_length = 200 , unique = True )
    # Add a checksum and add a unique Index to it
    
    def save(self):
        from FeedPaper.FP.controllers import calculate_checksum
        self.checksum = calculate_checksum(self.title + self.description + self.link_url)
        super ( itemDB , self ).save()
    
    def __unicode__(self):
        return self.title

class CSVUploadForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file  = forms.FileField()
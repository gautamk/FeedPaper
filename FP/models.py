from django.db import models

# Create your models here.
class feedDB(models.Model):
    keyword = models.CharField(max_length = 200)
    url = models.URLField()
    time_stamp = models.DateTimeField(auto_now = True)
    def __unicode__(self):
        return self.keyword
    
class itemDB(models.Model):
    feed = models.ForeignKey('feedDB')
    title = models.CharField(max_length = 200)
    description = models.TextField()
    link_url = models.URLField()
    time_stamp = models.DateTimeField(auto_now = True)
    def __unicode__(self):
        return self.title
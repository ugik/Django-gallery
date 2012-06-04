from django.db import models
from datetime import datetime

class PhotoUrl(models.Model):
    url = models.CharField(max_length=128)
    uploaded = models.DateTimeField()
    
    def save(self):
        print("Trying to Save")
        self.uploaded = datetime.now()
        models.Model.save(self)
        
    def __unicode__(self):
        return self.url

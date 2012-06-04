import mimetypes
from django import forms
from django.shortcuts import render_to_response
from django.template import Context
from django.template import RequestContext
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from models import PhotoUrl

class UploadForm(forms.Form):
    file = forms.ImageField(label='Select photo to upload')

def index(request):
    def store_in_s3(filename, content):
        conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        b = conn.create_bucket("ugik_images")
        mime = mimetypes.guess_type(filename)[0]
        k = Key(b)
        k.key = "photos/"+filename
        k.set_metadata("Content-Type", mime)
        k.set_contents_from_string(content)
        k.set_acl("public-read")
                
    photos = PhotoUrl.objects.all().order_by("-uploaded")
    if not request.method == "POST":
        f = UploadForm()
        return render_to_response("templates/index.html", {"form":f, "photos":photos}, context_instance=RequestContext(request))

    f = UploadForm(request.POST, request.FILES)
    if not f.is_valid():
        return render_to_response("templates/index.html", {"form":f, "photos":photos}, context_instance=RequestContext(request))

    file = request.FILES["file"]
    filename = file.name
    content = file.read()
    store_in_s3(filename, content)
    p = PhotoUrl(url="https://s3.amazonaws.com/ugik_images/photos/" + filename)
    p.save()
    photos = PhotoUrl.objects.all().order_by("-uploaded")
    return render_to_response("templates/index.html", {"form":f, "photos":photos}, context_instance=RequestContext(request))
    
    

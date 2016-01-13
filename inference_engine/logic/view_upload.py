# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from logic.forms import DocumentForm
from django.conf import settings
from os import listdir
from os.path import isfile, join
import os
def handle_uploaded_file(f):
    with open(os.path.join(settings.MEDIA_ROOT,f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            #newdoc = Document(docfile = request.FILES['docfile'])
            #newdoc.save()
            try:
                handle_uploaded_file(request.FILES['docfile'])

            except:
                pass
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('logic.view_upload.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    #documents = Document.objects.all()
    documents = [f for f in listdir(settings.MEDIA_ROOT) if isfile(join(settings.MEDIA_ROOT, f))]
    # Render list page with the documents and the form
    return render_to_response(
        'logic/list.html',
        {'form': form,'documents':documents},
        context_instance=RequestContext(request)
    )
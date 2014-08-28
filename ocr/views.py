import subprocess

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from roche.settings import MEDIA_ROOT

from .forms import UploadFileForm
from .models import UploadFile


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file=request.FILES['file'])
            new_file.save()

            file_name = '/' + unicode(new_file.file)
            print file_name
            # Call tesseract
            cmd_exit = subprocess.call(["/usr/bin/tesseract",
                                       MEDIA_ROOT + file_name,
                                       MEDIA_ROOT + file_name,
                                       "-l", "chi_tra"])
            if cmd_exit == -1:
                error_msg = "Tesseract error"
            else:
                error_msg = ""

            print error_msg

            f = open(MEDIA_ROOT + "/" + file_name + ".txt")
            print f.read()
            print new_file.file
            ocr_id = '123123'
            return HttpResponseRedirect(reverse('ocr.views.show_processed', args=(ocr_id,)))
    else:
        form = UploadFileForm()

    data = {'form': form }
    return render_to_response('ocr/index.html', data,
                              context_instance=RequestContext(request))

def show_processed(request, ocr_id):
    tesseract = 'TEST'
    data = {'tesseract': tesseract }
    return render_to_response('ocr/processed.html', data,
                              context_instance=RequestContext(request))

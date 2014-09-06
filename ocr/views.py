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

            # Call tesseract
            cmd_exit = subprocess.call(["/usr/bin/tesseract",
                                       MEDIA_ROOT + file_name,
                                       MEDIA_ROOT + file_name,
                                       "-l", "chi_tra"])
            if cmd_exit == -1:
                error_msg = "Tesseract error"
            else:
                error_msg = ""

            f = open(MEDIA_ROOT + "/" + file_name + ".txt")
            new_file.text = f.read()
            new_file.save()

            ocr_id = new_file.id

            return HttpResponseRedirect(reverse('ocr.views.show_processed', args=(ocr_id,)))
    else:
        form = UploadFileForm()

    data = {'form': form }
    return render_to_response('ocr/index.html', data,
                              context_instance=RequestContext(request))

def show_processed(request, ocr_id):
    try:
        ocr = UploadFile.objects.get(pk=int(ocr_id))
        tesseract = ocr.text
    except:
        tesseract = ''


    data = {'tesseract': tesseract}
    return render_to_response('ocr/processed.html', data,
                              context_instance=RequestContext(request))

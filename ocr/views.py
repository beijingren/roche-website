from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import UploadFileForm
from .models import UploadFile


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print request.FILES['file']
            new_file = UploadFile(file = request.FILES['file'])
            new_file.save()

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

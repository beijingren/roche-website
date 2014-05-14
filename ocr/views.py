from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from .forms import UploadFileForm
from .models import UploadFile


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file = request.FILES['file'])
            new_file.save()
            return HttpResponse("OK")
    else:
        form = UploadFileForm()

    data = {'form': form }
    return render_to_response('ocr/index.html', data, context_instance=RequestContext(request))

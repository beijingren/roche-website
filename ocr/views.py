from django.shortcuts import render_to_response

from .forms import UploadFileForm


def index(request):
    if request.method == 'POST':
        pass
    else:
        form = UploadFileForm()

    data = {'form': form }
    return render_to_response('ocr/index.html', data)

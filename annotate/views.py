from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import TextAnnotationForm


def index(request):
    
    if request.method == 'POST':
        pass
    else:
        form = TextAnnotationForm()

    data = {'form': form }
    return render_to_response('annotate/index.html', data, context_instance=RequestContext(request))

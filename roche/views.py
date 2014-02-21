from django.shortcuts import render
from django.template import RequestContext


def index(request):
    # XML and SPARQL numbers
    # Page should be cached

    data = {'number_texts': 4, 'number_authors': 4}
    return render(request, 'roche/index.html', data)

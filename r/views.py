# coding=utf-8
import re
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet
from eulxml.xmlmap.teimap import Tei

from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import SPARQLWrapper2
from SPARQLWrapper import JSON

from browser.models import RocheTEI
from common.utils import XSL_TRANSFORM_1
from common.utils import XSL_TRANSFORM_2
from common.utils import RE_INTERPUCTION

from roche.settings import FUSEKI_QUERY_URL


def text_info(request, title):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)

    qs = qs.filter(title=title)

    result = ""
    place_names = []
    persons = []
    terms = []
    chapter_titles = []
    for q in qs:

        number_characters = 0
        for d in q.body.div:
            text = re.sub(RE_INTERPUCTION, '', d.text)
            text = text.replace("\n", "")
            #text = text.replace("", "")
            number_characters += len(text)


        chapter_titles.append([q.chapter,
                               q.chapter_title.replace(" ", "").replace("\n", "")[:70],
                               number_characters])

        place_names.extend(q.place_names)
        persons.extend(q.persons)
        terms.extend(q.terms)

    place_names = list(set(place_names))
    persons = list(set(persons))
    terms = list(set(terms))

    # Place names for leaflet
    # place_names
    js_data = json.dumps([[[50.5, 30.5], "test"]])

    return render_to_response('browser/text_view_info.html', {'tei_documents': qs,
                              'tei_transform': result, 'place_names': place_names,
                              'persons': persons, 'terms': terms, 'js_data': js_data,
                              'chapter_titles': sorted(chapter_titles)})

# TODO: colored pdf
def text_download(request, title, file_format, juan=0):
    """
    Download a text or a single chapter as plain text file
    or as a (colored) pdf.
    """
    import pinyin

    pinyin_title = pinyin.get(title)

    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI',
                  collection='docker/texts/', model=RocheTEI)

    qs = qs.filter(title=title)
    if juan:
        qs = qs.filter(chapter=juan)


    result = ""
    for q in qs:
        for d in q.body.div:
            result += d.text.replace(" ", "").replace("\n", "").replace("\t", "").replace(u"。", u"。\n\n")

    if file_format == 'txt':
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="{}.txt"'.format(pinyin_title)
        response.write(result)
    else:
        from fpdf import FPDF

        pdf = FPDF(unit='mm', format='A4')
        pdf.add_page()
        pdf.add_font('Droid', '', 'DroidSansFallbackFull.ttf', uni=True)
        pdf.set_font('Droid', '', 12)
        pdf.write(5, unicode(result))
        response = HttpResponse(pdf.output(dest='S'), content_type='application/pdf') 
        response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(pinyin_title)

    return response


SPARQL_TIMELINE_QUERY = u"""
    PREFIX : <http://example.org/owl/sikuquanshu#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT
        (strafter(str(?subject), str(:)) AS ?person)
        (str(?birthY) AS ?birthYear)
        (str(?deathY) AS ?deathYear)
    {
        ?subject rdf:type :Person ;
        :birthYear ?birthY ;
        :deathYear ?deathY .
    }
    ORDER BY xsd:integer(?birthYear)
"""

def visual_timeline(request, title, juan):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)
    qs = qs.filter(title=title, chapter=juan)

    persons = []
    for q in qs:
        persons.extend(q.persons)

    sparql = SPARQLWrapper2(FUSEKI_QUERY_URL)
    sparql.setQuery(SPARQL_TIMELINE_QUERY)

    try:
        sparql_result = sparql.query()
    except:
        sparql_result = {}

    sparql_persons = {} 
    for binding in sparql_result.bindings:
         sparql_persons[binding[u"person"].value] = [binding[u"birthYear"].value, binding[u"deathYear"].value]

    #persons = [u"范仲淹", u"蘇舜欽", u"韓愈"]
    timeline_persons = []
    for p in set(persons):
        if sparql_persons.get(p, None):
             row = [p, ]
             row.append(int(sparql_persons[p][0]))
             row.append(int(sparql_persons[p][1]))
             timeline_persons.append(row)

    from operator import itemgetter

    timeline_persons = sorted(timeline_persons, key=itemgetter(1))
    timeline_persons = json.dumps(timeline_persons)

    return render_to_response('r/visual_timeline.html', {'tei_documents': qs, 'timeline_persons': timeline_persons, 'juan': juan, })

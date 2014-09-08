# coding=utf-8
import re
import json

from django.shortcuts import render_to_response

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet
from eulxml.xmlmap.teimap import Tei

from browser.models import RocheTEI
from common.utils import XSL_TRANSFORM_1
from common.utils import RE_INTERPUCTION


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
            text = text.replace("", "")
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
    js_data = json.dumps([[[50.5, 30.5], "test"]])

    return render_to_response('browser/text_view_info.html', {'tei_documents': qs,
                              'tei_transform': result, 'place_names': place_names,
                              'persons': persons, 'terms': terms, 'js_data': js_data,
                              'chapter_titles': sorted(chapter_titles)})

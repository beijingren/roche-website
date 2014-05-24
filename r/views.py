from django.shortcuts import render_to_response

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet
from eulxml.xmlmap.teimap import Tei

from browser.models import RocheTEI
from common.utils import XSL_TRANSFORM_1


def text_info(request, title):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)

    qs = qs.filter(title=title)

    result = ""
    place_names = []
    persons = []
    terms = []
    chapter_titles = []
    for q in qs:
        chapter_titles.append([q.chapter, q.chapter_title.replace(" ", "").replace("\n", "")[:70]])

        place_names.extend(q.place_names)
        persons.extend(q.persons)
        terms.extend(q.terms)

    place_names = list(set(place_names))
    persons = list(set(persons))
    terms = list(set(terms))

    return render_to_response('browser/text_view_info.html', {'tei_documents': qs,
                              'tei_transform': result, 'place_names': place_names,
                              'persons': persons, 'terms': terms,
                              'chapter_titles': sorted(chapter_titles)})

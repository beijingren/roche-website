# coding=utf8

from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON

from roche.settings import FUSEKI_UPDATE_URL

from .common import SPARQL_LOCAL_UPDATE_HEADER
from .common import SPARQL_LOCAL_UPDATE_FOOTER


#
# person is in SPARQL JSON
#
# TODO: should be more abstract
#
def sparql_local_insert_person(lemma, person):

    query = SPARQL_LOCAL_UPDATE_HEADER

    query += u":{} rdfs:type owl:NamedIndividual .\n".format(lemma)
    if person['dateOfBirth']['value']:
        query += u":{} :birthYear \"{}\"^^xsd:integer .\n".format(lemma, person['dateOfBirth']['value'])
    if person['dateOfDeath']['value']:
        query += u":{} :deathYear \"{}\"^^xsd:integer .\n".format(lemma, person['dateOfDeath']['value'])

    query += SPARQL_LOCAL_UPDATE_FOOTER
    print query

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(query)
    sparql.method = 'POST'
    sparql.query()

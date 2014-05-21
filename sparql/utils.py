# coding=utf8
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

    query += u":{} rdfs:type owl:NamedIndividual .".format(lemma)
    if person['dateOfBirth']['value']:
        query += u":{} :birthYear \"{}^^xsd:integer\"".format(lemma, result['dateOfBirth']['value'])
    if result['dateOfDeath']['value']:
        query += u":{} :deathYear \"{}^^xsd:integer\"".format(lemma, result['dateOfDeath']['value'])

    query += SPARQL_LOCAL_UPDATE_FOOTER

    sparql = SPARQLWrapper(FUSEKI_UPDATE_URL)
    sparql.setQuery(update_query)
    sparql.method = 'POST'
    sparql.query()

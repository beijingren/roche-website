# coding=utf8

import requests
from django.shortcuts import render

from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON

from roche.settings import FUSEKI_QUERY_URL
from roche.settings import FUSEKI_UPDATE_URL


prefix_default = "http://example.org/owl/sikuquanshu#"
prefix_schema = "http://www.w3.org/2000/01/rdf-schema#"
prefix_syntax = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

sparql_query = u"""
    PREFIX : <http://example.org/owl/sikuquanshu#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT *
    WHERE {{ :{0} ?p ?o . }}"""

#    ?s dbpprop:t "{}"@en ;
#    ?s rdfs:label "{}" ;
SPARQL_DBPEDIA_QUERY = u"""
    PREFIX dbpprop: <http://dbpedia.org/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT *
    WHERE {{
    ?s dbpprop:t "{}"@en ;
    dbpprop:dateOfBirth ?dateOfBirth ;
    dbpprop:dateOfDeath ?dateOfDeath .
    }}
    """

SPARQL_FUSEKI_UPDATE_QUERY = u"""
    PREFIX : <http://example.org/owl/sikuquanshu#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT DATA {
    """

CBDB_API_URL = u"http://cbdb.fas.harvard.edu/cbdbapi/person.php?name={}&o=json"
DBPEDIA_QUERY_URL = "http://dbpedia.org/sparql/query"

#
# Only look and insert canonical names.  Hao, zi names should be handled
# in tagging process.
#
def index(request, lemma):
    from django.http import HttpResponse
    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(sparql_query.format(lemma))
    sparql.setReturnFormat(JSON)

    try:
        sparql_results = sparql.queryAndConvert()
    except:
        sparql_results = {}

    #
    # Check if we found something in our own sparql repository.  If not
    # query other sources.
    #
    # TODO: We need a better check (persons with the same name).
    #
    #if not sparql_results or not sparql_results["results"]["bindings"]:
    if True:

        #
        # DBPEDIA
        #
        sparql = SPARQLWrapper(DBPEDIA_QUERY_URL)
        sparql.setQuery(SPARQL_DBPEDIA_QUERY.format(lemma))
        sparql.setReturnFormat(JSON)

        try:
            sparql_results = sparql.queryAndConvert()
        except:
            import traceback
            print traceback.format_exc()
            sparql_results = {}

        print "DBPEDIA"
        print SPARQL_DBPEDIA_QUERY.format(lemma)
        print sparql_results

        if sparql_results and sparql_results["results"]["bindings"]:
            for result in sparql_results["results"]["bindings"]:
                from .utils import sparql_local_insert_person

                sparql_local_insert_person(lemma, result)


        #
        # CBDB
        #
        r = requests.get(CBDB_API_URL.format(lemma)).json()
        #if r.status_code == 200:
        try:
            persons = r['Package']['PersonAuthority']['PersonInfo']['Person']
        except:
            persons = []

        if type(persons) is list:
            for person in persons:
                print person['BasicInfo']['ChName'], person['BasicInfo']['YearBirth'], person['BasicInfo']['PersonId']
        else:
            person = persons
            if person:
                print person['BasicInfo']['ChName'], person['BasicInfo']['YearBirth'], person['BasicInfo']['PersonId']

            return HttpResponse("Found persons")

        return HttpResponse("SPARQL INSERT")

    is_person = False
    template_result = {}
    for result in sparql_results["results"]["bindings"]:
        p = result["p"]["value"].replace(prefix_default, '')
        p = p.replace(prefix_schema, '')
        p = p.replace(prefix_syntax, '')

        o = result["o"]["value"].replace(prefix_default, '')

        if p == "type" and o == "Person":
            is_person = True

        template_result[p] = o

    template_result['is_person'] = is_person
    template_result['lemma'] = lemma

    return render(request, 'sparql/index.html', {'r': template_result})

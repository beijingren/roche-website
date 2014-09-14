# coding=utf8

import requests
import wikipedia
import creole
import codecs

from django.http import HttpResponse
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
#DBPEDIA_QUERY_URL = "http://dbpedia.org/sparql/query"
DBPEDIA_QUERY_URL = "http://dbpedia-live.openlinksw.com/sparql"

#
# Only look and insert canonical names.  Hao, zi names should be handled
# in tagging process.
#
def index(request, lemma):

    #
    # Check if we found something in our own sparql repository.  If not
    # query other sources.
    #
    # TODO: We need a better check (persons with the same name).
    #
    #if not sparql_results or not sparql_results["results"]["bindings"]:
    if False:

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

        #if sparql_results and sparql_results["results"]["bindings"]:
        #    for result in sparql_results["results"]["bindings"]:
        #        from .utils import sparql_local_insert_person
        #
        #        sparql_local_insert_person(lemma, result)
        #else:

        if True:
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


        sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
        sparql.setQuery(sparql_query.format(lemma))
        sparql.setReturnFormat(JSON)

        try:
            sparql_results = sparql.queryAndConvert()
        except:
            sparql_results = {}

    sparql = SPARQLWrapper(FUSEKI_QUERY_URL)
    sparql.setQuery(sparql_query.format(lemma))
    sparql.setReturnFormat(JSON)

    try:
        sparql_results = sparql.queryAndConvert()
    except:
        sparql_results = {}

    is_person = False
    template_result = {}
    if sparql_results.get("results", False):
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

    # Wikipedia
    try:
        wikipedia.set_lang("en")
        en = wikipedia.page(lemma, auto_suggest=True, redirect=True)
        wikipedia_en = en.summary
        wikipedia_en_url = en.url
    except:
        wikipedia_en = ''
        wikipedia_en_url = ''

    try:
        wikipedia.set_lang("zh")
        zh = wikipedia.page(lemma, auto_suggest=True, redirect=True)
        wikipedia_zh = zh.summary
        wikipedia_zh_url = zh.url
    except:
        wikipedia_zh = ''
        wikipedia_zh_url = ''

    # Sinology
    try:
        f = codecs.open("/docker/dublin-store/sinology/mainSpace/" + lemma, "r", "utf-8")
        # Skip first line
        sinology = f.readlines()[1:]
        sinology = '\n'.join(sinology)
        sinology = creole.creole2html(sinology)
    except:
        sinology = ''

    return render(request, 'sparql/index.html', {'r': template_result,
                  'wikipedia_en': wikipedia_en,
                  'wikipedia_zh': wikipedia_zh,
                  'wikipedia_en_url': wikipedia_en_url,
                  'wikipedia_zh_url': wikipedia_zh_url,
                  'sinology': sinology,
                  })

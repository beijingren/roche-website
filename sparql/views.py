from django.shortcuts import render

from SPARQLWrapper import SPARQLWrapper
from SPARQLWrapper import JSON
from roche.settings import FUSEKI_SERVER_URL


prefix_default = "http://example.org/owl/sikuquanshu#"
prefix_schema = "http://www.w3.org/2000/01/rdf-schema#"
prefix_syntax = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

sparql_query = u"""
    PREFIX : <http://example.org/owl/sikuquanshu#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT *
    WHERE {{ :{0} ?p ?o . }}"""

def index(request, lemma):
    sparql = SPARQLWrapper(FUSEKI_SERVER_URL)
    sparql.setQuery(sparql_query.format(lemma))
    sparql.setReturnFormat(JSON)

    try:
        sparql_results = sparql.query().convert()
    except:
        sparql_results = {}

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

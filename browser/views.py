# coding=utf-8
from django.shortcuts import render_to_response

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet
from eulxml.xmlmap.teimap import Tei


XSL_TRANSFORM_1 = '''<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="1.0">

<xsl:output method="html" omit-xml-declaration="yes" indent="no" />

<xsl:template match="/">
<div>
<xsl:apply-templates/>
</div>
</xsl:template>

<xsl:template match="tei:div">
<p>
    <xsl:apply-templates/>
</p>
</xsl:template>

<xsl:template match="tei:persName">
<a class="persName"><xsl:attribute name="href">/wiki/<xsl:value-of select="." />#persName</xsl:attribute> 
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:placeName">
<a class="placeName" style="color: red;" href="">
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:term">
<a class="term" style="color: green;" href="">
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:l">
<span class="term" style="background-color: Gainsboro;">
<xsl:value-of select="."/>
</span>
</xsl:template>

</xsl:stylesheet>
'''


def index(request):
    from browser.models import RocheTEI

    qs = QuerySet(using=ExistDB(), xpath='/*:TEI', model=RocheTEI)

    return render_to_response('browser/index.html', {'tei_documents': qs})


def index_author(request, letter):
    qs = QuerySet(using=ExistDB(), xpath='/*:TEI', model=Tei)

    # filter by authors starting with letter
    gs = gs.filter(author__startswith=letter)

    return render_to_response('browser/index.html', {'tei_documents': qs})


def index_title(request, letter):
    qs = QuerySet(using=ExistDB(), xpath='/*:TEI', model=Tei)

    # filter by titles starting with letter
    qs = qs.filter(title__startswith=letter)

    return render_to_response('browser/index.html', {'tei_documents': qs})


def text_view(request, title):
    qs = QuerySet(using=ExistDB(), xpath='/*:TEI', model=Tei)

    # filter by title
    qs = qs.filter(title=title)
    result = qs[0].body.xsl_transform(xsl=XSL_TRANSFORM_1)

    return render_to_response('browser/text_view.html', {
                              'tei_transform': result.serialize()})

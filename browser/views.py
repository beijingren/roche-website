# coding=utf-8
from django.shortcuts import render_to_response

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet
from eulxml.xmlmap.teimap import Tei

from browser.models import RocheTEI


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
<p style="margin: 0 0 4%;">
    <xsl:apply-templates/>
</p>
</xsl:template>

<xsl:template match="tei:persName">
<a class="persName"><xsl:attribute name="href">/sparql/<xsl:value-of select="." />#persName</xsl:attribute> 
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:placeName">
<a class="placeName" style="color: red;"><xsl:attribute name="href">/wiki/<xsl:value-of select="." />#placeName</xsl:attribute>
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:term">
<a class="term" style="color: green;"><xsl:attribute name="href">/wiki/<xsl:value-of select="." />#term</xsl:attribute>
<xsl:value-of select="."/>
</a>
</xsl:template>

<!--
<xsl:template match="tei:lg[@type='poem']">
<h1>
<xsl:value-of select="tei:head"/>
</h1>
</xsl:template>
-->

<xsl:template match="tei:head">
<h1 style="background-color: grey;">
<xsl:value-of select="."/>
</h1>
</xsl:template>

<xsl:template match="tei:l[../@type='poem' or ../../@type='poem']">
<xsl:value-of select="."/>
<br/>
</xsl:template>

<xsl:template match="tei:l|tei:time">
<span class="term" style="background-color: Gainsboro;">
<xsl:value-of select="."/>
</span>
</xsl:template>

</xsl:stylesheet>
'''


def index(request):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)
    qs = qs.only('title', 'title_en', 'author')

    return render_to_response('browser/index.html', {'tei_documents': qs})


def index_author(request, author, startswith):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=Tei)

    if startswith:
        # filter by authors starting with letter
        qs = qs.filter(author__startswith=author)
    else:
        qs = qs.filter(author=author)

    return render_to_response('browser/index.html', {'tei_documents': qs})


def index_title(request, letter):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=Tei)

    # filter by titles starting with letter
    qs = qs.filter(title__startswith=letter)

    return render_to_response('browser/index.html', {'tei_documents': qs})


def text_view(request, title):
    qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/texts/', model=RocheTEI)

    # filter by title
    qs = qs.filter(title=title)
    result = qs[0].body.xsl_transform(xsl=XSL_TRANSFORM_1)

    return render_to_response('browser/text_view.html', {'tei_documents': qs,
                              'tei_transform': result.serialize()})

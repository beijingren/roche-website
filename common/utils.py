# coding=utf-8
RE_INTERPUCTION = u"[，。！、“”「」：？《》]"

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

<xsl:template match="tei:div[@type='chapter']">
<h1 style="text-align: center; color: grey; margin: 20px 0px 30px 0px;">
<xsl:value-of select="@n"/>
</h1>
<xsl:apply-templates/>
</xsl:template>

<xsl:template match="tei:div">
<p style="margin: 0 0 4%;">
    <xsl:apply-templates/>
</p>
</xsl:template>

<xsl:template match="tei:name">
<a class="name" data-toggle="tooltip">
<xsl:attribute name="href">/sparql/<xsl:value-of select="@key" /></xsl:attribute>
<xsl:attribute name="title">
<xsl:value-of select="@key" />
</xsl:attribute>
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:persName">
<a class="persName"><xsl:attribute name="href">/sparql/<xsl:value-of select="." />#persName</xsl:attribute> 
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:placeName">
<a class="placeName"><xsl:attribute name="href">/sparql/<xsl:value-of select="." />#placeName</xsl:attribute>
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:term">
<a class="term"><xsl:attribute name="href">/wiki/<xsl:value-of select="." />#term</xsl:attribute>
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:title">
<a class="title"><xsl:attribute name="href">/wiki/<xsl:value-of select="." />#title</xsl:attribute>
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:quote">
<span class="quote">
<xsl:value-of select="."/>
</span>
</xsl:template>

<xsl:template match="tei:pc">
<span class="pc">
<xsl:value-of select="."/>
</span>
</xsl:template>

<!--
<xsl:template match="tei:lg[@type='poem']">
<h1>
<xsl:value-of select="tei:head"/>
</h1>
</xsl:template>
-->

<xsl:template match="tei:head">
<h1>
<xsl:value-of select="."/>
</h1>
<hr/>
</xsl:template>

<xsl:template match="tei:l[../@type='poem' or ../../@type='poem']">
<xsl:value-of select="."/>
<br/>
<xsl:apply-templates/>
<br/>
</xsl:template>

<xsl:template match="tei:rhyme[@type='平' and string-length(@label) > 0]">
<span class="rhyme" style="background-color: black; color: white;">
<xsl:value-of select="@label"/>
</span>
</xsl:template>

<xsl:template match="tei:rhyme[@type='平' and string-length(@label) = 0]">
<span class="rhyme" style="background-color: black; color: black;">
<xsl:value-of select="."/>
</span>
</xsl:template>

<xsl:template match="tei:rhyme[@type!='平' and string-length(@label) > 0]">
<span class="rhyme" style="background-color: red; color: white;">
<xsl:value-of select="@label"/>
</span>
</xsl:template>

<xsl:template match="tei:rhyme[@type!='平' and string-length(@label) = 0]">
<span class="rhyme" style="background-color: red; color: red;">
<xsl:value-of select="."/>
</span>
</xsl:template>

<xsl:template match="tei:l|tei:time">
<span class="time" data-toggle="tooltip">
<xsl:attribute name="title">
<xsl:value-of select="@when" />
</xsl:attribute>
<xsl:value-of select="."/>
</span>
</xsl:template>

<xsl:template match="tei:date[@notBefore!='null']">
<span class="date" data-toggle="tooltip">
<xsl:attribute name="title">
<xsl:value-of select="@notBefore" /> - <xsl:value-of select="@notAfter" />
</xsl:attribute>
<xsl:value-of select="."/>
</span>
</xsl:template>

<xsl:template match="tei:date">
<span class="date" data-toggle="tooltip">
<xsl:attribute name="title">
<xsl:value-of select="@when" />
</xsl:attribute>
<xsl:value-of select="."/>
</span>
</xsl:template>

<xsl:template match="tei:pb">
<sup class="pb">
<xsl:value-of select="@n"/>
</sup>
</xsl:template>

<xsl:template match="tei:num">
<span class="num" data-toggle="tooltip">
<xsl:attribute name="title">
<xsl:value-of select="@value" />
</xsl:attribute>
<xsl:value-of select="."/>
</span>
</xsl:template>

<xsl:template match="tei:measure">
<span class="measure" data-toggle="tooltip">
<xsl:attribute name="title">
<xsl:value-of select="@quantity" />
<xsl:text>&#xA0;</xsl:text>
<xsl:value-of select="@unit" />
</xsl:attribute>
<xsl:value-of select="."/>
</span>
</xsl:template>

</xsl:stylesheet>
'''


XSL_TRANSFORM_2 = '''<?xml version="1.0" encoding="UTF-8" ?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="1.0">

<xsl:output method="text" omit-xml-declaration="yes" indent="no" />

<xsl:template match="tei:p">
<p>
<xsl:apply-templates/>
</p>
</xsl:template>

<xsl:template match="tei:persName|tei:placeName|tei:term|tei:title|tei:pc|tei:head|tei:l|tei:time">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="tei:l[../@type='poem' or ../../@type='poem']">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="tei:pb/@n">
<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="tei:num|tei:measure">
<xsl:value-of select="."/>
</xsl:template>
</xsl:stylesheet>
'''

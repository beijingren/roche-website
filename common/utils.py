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

<xsl:template match="tei:title">
<a class="term" style="color: green;"><xsl:attribute name="href">/wiki/<xsl:value-of select="." />#title</xsl:attribute>
<xsl:value-of select="."/>
</a>
</xsl:template>

<xsl:template match="tei:pc">
<span class="pc" style="color: Gray;">
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

<xsl:template match="tei:pb/@n">
<sup style="color:  SlateGray;">
<xsl:value-of select="."/>
</sup>
</xsl:template>

</xsl:stylesheet>
'''



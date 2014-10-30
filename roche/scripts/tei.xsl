<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
         xmlns:tei="http://www.tei-c.org/ns/1.0"
         exclude-result-prefixes="tei"
     version="1.0">

     <xsl:output encoding="utf-8" omit-xml-declaration="yes"
             indent="yes"/>

    <xsl:template match="/">
        <xsl:variable name="bibl" select="//tei:biblFull[1]"/>
        <doc>
            <field name='id'>XXX</field>
            <field name='title'><xsl:value-of 
select="//tei:titleStmt/tei:title"/></field>
            <!-- assumes 'creator' is a multi-valued field in your 
schema -->
            <xsl:for-each select="$bibl/tei:titleStmt/tei:author/tei:name">
                <field name='creator'><xsl:value-of select="."/></field>
            </xsl:for-each>
            <!-- other fields as appropriate -->

            <!-- this is a very 'brute force' and decidedly 
non-optimized approach to extracting the 'full text' from the document, 
as it just extracts the xpath value of the tei:text element (i.e. all 
the text underneath that element, irrespective of attributes).Note that 
the normalize-space() is optional, but it will be easier on your eyes if 
you ever need to inspect the results =) -->
            <field name='text'>
                <xsl:value-of select="normalize-space(//tei:text)"/></field>
        </doc>

    </xsl:template>
</xsl:stylesheet>

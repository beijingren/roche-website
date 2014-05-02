from eulxml import xmlmap
from eulxml.xmlmap import teimap


class RocheTEI(teimap.Tei):
    title_en  = xmlmap.StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@xml:lang="en"]')
    chapter = xmlmap.IntegerField('tei:text/tei:body/tei:div/@n')
    place_names = xmlmap.StringListField('//tei:placeName')
    persons = xmlmap.StringListField('//tei:persName')
    terms = xmlmap.StringListField('//tei:term')

    @property
    def first_letter_author(self):
        """Return the first letter of the authors surname"""

        return self.author

    @property
    def first_letter_title(self):
        """Return the first letter of the title"""

        return self.title


class DDBCPlaceName(teimap._TeiBase):
    place_names = xmlmap.StringListField('tei:placeName')
    district = xmlmap.StringField('tei:district')
    notes = xmlmap.StringListField('tei:note')
    geo = xmlmap.StringField('tei:location/tei:geo')

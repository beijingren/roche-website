from eulxml import xmlmap
from eulxml.xmlmap import teimap


class RocheTEI(teimap.Tei):
    title_en  = xmlmap.StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title[@xml:lang="en"]')

    @property
    def first_letter_author(self):
        """Return the first letter of the authors surname"""

        return self.author

    @property
    def first_letter_title(self):
        """Return the first letter of the title"""

        return self.title

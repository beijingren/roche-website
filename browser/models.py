from eulxml.xmlmap import teimap


class RocheTEI(teimap.Tei):

    @property
    def first_letter_author(self):
        """Return the first letter of the authors surname"""

        return self.author

    @property
    def first_letter_title(self):
        """Return the first letter of the title"""

        return self.title

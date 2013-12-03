from django import template

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet


register = template.Library()


class DDBCPlaceNameNode(template.Node):
    def __init__(self, place_name):
        self.place_name = template.Variable(place_name)

    def render(self, context):
        from browser.models import DDBCPlaceName

        try:
            self.place_name = self.place_name.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        qs = QuerySet(using=ExistDB(), xpath='/tei:TEI//tei:place', collection='docker/resources/', model=DDBCPlaceName)
        qs = qs.filter(place_names=self.place_name)

        ddbc_output = u''
        for q in qs:
            ddbc_output += '<p>'
            ddbc_output += 'Other names: ' + u', '.join(q.place_names) + '<br>'
            ddbc_output += 'District: ' + q.district + '<br>'
            ddbc_output += 'Notes: ' + u' '.join(q.notes) + '<br>'
            ddbc_output += 'Location: ' + q.geo + '<br>'
            ddbc_output += '</p>'

        return ddbc_output


@register.tag
def ddbc_place_name(parser, token):
    try:
        tag_name, place_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("requires single argument")

    return DDBCPlaceNameNode(place_name)




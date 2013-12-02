from django import template

from eulexistdb.db import ExistDB
from eulexistdb.query import QuerySet


register = template.Library()


class DDBCPlaceNameNode(template.Node):
    def __init__(self, place_name):
        self.place_name = template.Variable(place_name)

    def render(self, context):
        try:
            self.place_name = self.place_name.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        qs = QuerySet(using=ExistDB(), xpath='/tei:TEI', collection='docker/resources/')

        return self.place_name


@register.tag
def ddbc_place_name(parser, token):
    try:
        tag_name, place_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("requires single argument")

    return DDBCPlaceNameNode(place_name)




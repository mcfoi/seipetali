__author__ = 'elfo'

from django import template

register = template.Library()


@register.tag
def icanhaz(parser, token):
    nodelist = parser.parse(('endicanhaz',))
    parser.delete_first_token()
    return ICanHazNode(nodelist)

@register.tag
def angular(parser, token):
    nodelist = parser.parse(('endangular',))
    parser.delete_first_token()
    return ICanHazNode(nodelist)


class ICanHazNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context, ):
        output = self.nodelist.render(context)
        return output.replace('[[[', '{{{').replace(']]]', '}}}').replace('[[', '{{').replace(']]', '}}')
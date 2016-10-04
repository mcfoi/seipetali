from django import template

register = template.Library()


@register.simple_tag
def input_inner_label(id, name):
    return "$('#%s').blur(function(){if(this.value==''){this.value='%s'}}).focus(function(){if(this.value=='%s'){this.value=''}}).blur();"%(id, name, name)


@register.simple_tag
def autocomplete(id, api):
    return "$('#%s').autocomplete({source: \"%s\"})"%(id, api)


@register.simple_tag
def datepicker(id):
    return "$('#%s').datepicker()"%id

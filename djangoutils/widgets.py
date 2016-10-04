from django import forms
from django.forms.util import flatatt
from django.utils.safestring import mark_safe


__all__ = ('ForeignKeySelect', 'ManyToManySelect')


class ModelChoiceIterator(forms.models.ModelChoiceIterator):

    def __init__(self, field, ids=None):
        super(ModelChoiceIterator, self).__init__(field)
        if ids is not None:
            self.queryset = self.queryset.filter(id__in=ids)


class ForeignKeySelect(forms.widgets.Widget):

    def __init__(self, model_class, *args, **kwargs):
        self._model_class = model_class
        super(ForeignKeySelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        if value is None or value == '':
            value_str = ''
            pk = ''
        else:
            value_str = unicode(self._model_class.objects.get(pk=value))
            pk = unicode(value)
        final_attrs = self.build_attrs(attrs, type='text', name=name + '_display', readonly='readonly', value=value_str)
        if 'class' in final_attrs:
            final_attrs['class'] += ' textInput'
        else:
            final_attrs['class'] = 'textInput'
        html = [
            u'<ul class="alternate">',
            u'<li style="width:80%%"><input%s /></li>'%flatatt(final_attrs),
            u'<li style="width:12%%"><input type="submit" name="%s_get" class="submit submitButton" value="Get" style="margin-top:.5em" /></li>'%name,
            u'</ul>',
            u'<input type="hidden" name="%s" value="%s" />'%(name, pk),
        ]
        return mark_safe(u'\n'.join(html))


class ManyToManySelect(forms.CheckboxSelectMultiple):

    # class Media:
    #     js = ('js/jquery.min.js', 'address/js/address.js',)

    def __init__(self, *args, **kwargs):
        super(ManyToManySelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, **kwargs):
        if value is None:
            value = []

        intro = u'\n'.join([
            u'<ul>',
            u'<li><input type="submit" name="%s_select" value="Select" class="m2mselect-select submit submitButton"></input></li>'%name,
        ])
        outro = u'</ul>'

        # Replace the global choices with only the currently selected set, then
        # call the parent render function. Swap back afterwards.
        old_choices = self.choices
        self.choices = ModelChoiceIterator(self.choices.field, value)
        html = super(ManyToManySelect, self).render(name, value, attrs, **kwargs)
        self.choices = old_choices

        return mark_safe(u'\n'.join([intro, html, outro]))

    # def value_from_datadict(self, data, files, name):
    #     return data

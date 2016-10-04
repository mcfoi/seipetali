from uni_form.helpers import *


def make_helper(form, primary_buttons=[], secondary_buttons=[]):
    helper = FormHelper()
    layout = Layout(Fieldset('', *[f.name for f in form.visible_fields()]))
    for name, text in primary_buttons:
        btn = Submit(name, text, css_class='primaryAction')
        helper.add_input(btn)
    for name, text in secondary_buttons:
        btn = Submit(name, text, css_class='secondaryAction')
        helper.add_input(btn)
    helper.form_action = ''
    helper.form_method = 'POST'
    helper.form_style = 'inline'
    helper.add_layout(layout)
    return helper


class UniFormMedia(object):

    class Media:
        css = {'all': ('uni_form/uni-form.css', 'uni_form/default.uni-form.css')}
        js = ('js/jquery.min.js', 'uni_form/uni-form.jquery.js')

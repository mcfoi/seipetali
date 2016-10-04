__author__ = 'elfo'

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


from django.forms.widgets import DateInput,force_text,flatatt,format_html





class DateInputAngularBootstrapDatepicker(DateInput):


    def render(self, name, value, attrs=None):

        # ng-model='checkin' is-open="opened" ng-focus="opened=true" datepicker-popup

        # or

        # <p class="input-group">
        #   <input type="text" class="form-control" ng-model='checkin' is-open="opened" ng-focus="opened=true" datepicker-popup  />
        #   <span class="input-group-btn">
        #     <button type="button" class="btn btn-default" ng-click="opened=true;$event.stopPropagation()"><i class="glyphicon glyphicon-calendar"></i></button>
        #   </span>
        # </p>

        attrs['ng-model'] = attrs['id']
        attrs['is-open'] = "%s_opened" % attrs['id']
        attrs['ng-focus'] = "%s_opened=true" % attrs['id']

        if value is None:
            value = ''

        attrs['ng-init'] = "%s='%s'" % (attrs['ng-model'],value)

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))

        # print final_attrs
        # print flatatt(final_attrs)
        # print format_html('<input{0} datepicker-popup/>', flatatt(final_attrs))


        return format_html('<input{0} datepicker-popup/>', flatatt(final_attrs))

    # def render(self, name, value, attrs=None):
    #     if value is None:
    #         value = ''
    #     final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
    #     if value != '':
    #         # Only add the 'value' attribute if a value is non-empty.
    #         final_attrs['value'] = force_text(self._format_value(value))
    #     return format_html('<input{0} />', flatatt(final_attrs))


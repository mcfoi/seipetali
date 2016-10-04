from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext

from notification import backends
# from django.contrib.sites.models import Site
# from django.core.urlresolvers import reverse
from requests.exceptions import ConnectionError

from django.core.mail import EmailMultiAlternatives
# from celery_tasks.tasks import send_email
from django.contrib.auth import get_user_model


class EmailBackend(backends.BaseBackend):
    spam_sensitivity = 2
    
    def can_send(self, user, notice_type):
        can_send = super(EmailBackend, self).can_send(user, notice_type)
        if can_send and user.email:
            return True
        return False

    def deliver_to_recipient_email(self, recipient, sender, notice_type, extra_context):
        User = get_user_model()
        fake_user = User(email=recipient)
        self.deliver(fake_user, sender, notice_type, extra_context)

    def deliver(self, recipient, sender, notice_type, extra_context):
        # TODO: require this to be passed in extra_context

        # print 'EmailBackend deliver()'

        # current_site = Site.objects.get_current()
        # notices_url = u"http://%s%s" % (
        #     unicode(Site.objects.get_current()),
        #     reverse("settings"),
        # )

        context = self.default_context()

        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.display),
            # "notices_url": notices_url,
            # "current_site": current_site,

        })
        context.update(extra_context)



        # Ottine una lista messaggi nei vari template
        messages = self.get_formatted_messages((
            "short.txt",
            "short.html",
            "full.txt",
            "full.html"
        ), notice_type.label, context)
        # print "messages:", messages
        
        subject = "".join(render_to_string("notification/email_subject.txt", {
            "message": messages["short.txt"],
        }, context).splitlines())

        
        # body = render_to_string("notification/email_body.html", {
        #     "message": messages["full.html"],
        # }, context)


        text_content =  render_to_string("notification/email_body.txt", {
            "message": messages["full.txt"],
        }, context)

        html_content =  render_to_string("notification/email_body.html", {
            "message": messages["full.html"],
        }, context)




        # Send directly
        # msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [recipient.email])
        # msg.attach_alternative(html_content, "text/html")
        # print msg
        # msg.send()




        # send by celery
        msg_data = {
            'subject':subject,
            'text_content':text_content,
            'html_content':html_content,
            'from_email':settings.DEFAULT_FROM_EMAIL,
            'recipients':[recipient.email],
        }

        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [recipient.email])
        msg.attach_alternative(html_content, "text/html")
        # print msg
        msg.send()

        # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient.email])


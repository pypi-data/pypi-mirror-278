from datetime import datetime as dt
import logging

import os

from django.core.mail import EmailMessage
from botocore.exceptions import ClientError


from django.core.management.base import (BaseCommand, CommandParser,
                                         CommandError)

from openlxp_notifications.models import (email)

from openlxp_notifications.management.utils.ses_configuration import (
    overall_health)


logger = logging.getLogger('dict_config_logger')

TEMPLATE_ROOT = os.path.abspath(os.path.join(__file__, "../../.."))


def trigger_health_check():
    """Command to trigger email health check"""
    overall_health()


def trigger_subscribed_list_update(email_type, recipient_list, owner,
                                   list_name, list_url):
    """Command to trigger email for list updates"""

    trigger_health_check()

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = email_type.sender

    # The subject line for the email.
    SUBJECT = email_type.subject

    # The HTML body of the email.
    now = dt.now()
    datetimenow = now.strftime("%d/%m/%Y %H:%M:%S")
    for each_recipient in recipient_list:
        try:
            MESSAGE_HTML = email_type.template_type.message
            BODY_HTML = \
                open(TEMPLATE_ROOT +
                     '/templates/status_update_template.html').read()

            email = each_recipient[0]
            name = each_recipient[1] + " " + each_recipient[2]

            BODY_HTML = BODY_HTML.format(message=MESSAGE_HTML)
            BODY_HTML = BODY_HTML.format(name=name, date_time=datetimenow,
                                         author=owner, list_name=list_name,
                                         list_url=list_url)

            mail = EmailMessage(SUBJECT, BODY_HTML, SENDER,
                                [email])
            mail.content_subtype = "html"
            mail.send()
        # Display an error if something goes wrong.
        except ClientError as e:
            logger.error(e.response['Error']['Message'])
            continue


class Command(BaseCommand):
    """Django command to send an emails to the filer/personas, when the log
    warning/error occurred in the metadata EVTVL process."""

    def add_arguments(self, parser: CommandParser) -> None:
        # parser.add_argument('email_references', nargs="+", type=str)
        parser.add_argument('email_references', type=str)
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        """Email log notification is sent to filer/personas when warning/error
        occurred in EVTVL process"""
        # for email_reference in options['email_references']:
        try:
            email_type = email.objects.get(
                reference=options['email_references'])
        except email.DoesNotExist:
            raise CommandError('Email Reference "%s" does not exist' %
                               options['email_references'])

        recipient_list = [('kjijo@deloitte.com', 'Karen', 'Jijo'),
                          ('karenjijo@gmail.com', 'Karen', 'J')]
        trigger_health_check()
        trigger_subscribed_list_update(email_type, recipient_list, "Owner",
                                       "List1",
                                       "https://dev-xds.deloitteopenlxp.com/"
                                       "lists/1")

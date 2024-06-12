from django.db import models
from model_utils.models import TimeStampedModel

from openlxp_notifications.management.utils.ses_client import (
    email_verification)


class recipient(models.Model):
    """Model for POC Email Configuration """

    first_name = models.CharField(max_length=200,
                                  help_text='Enter recipient name',
                                  null=False, blank=False)
    last_name = models.CharField(max_length=200,
                                 help_text='Enter recipient name',
                                 null=False, blank=False)
    email_address = models.EmailField(
        max_length=254,
        help_text='Enter recipient Email ID',
        unique=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.email_address}'

    def save(self, *args, **kwargs):
        email_verification()
        return super(recipient, self).save(*args, **kwargs)


class subject(TimeStampedModel):
    """Model for Subject set up"""
    subject = models.CharField(max_length=200,
                               default='OpenLXP Conformance Alerts',
                               help_text="Enter Subject for email")

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.subject}'


class template(TimeStampedModel):
    """Model for template set up"""
    template_id = models.BigAutoField(primary_key=True)
    template_type = models.CharField(max_length=200,
                                     help_text='Enter Template Type',
                                     unique=True, null=False, blank=False)
    message = models.TextField(help_text="Enter Email Message",
                               blank=True, null=True,)
    template_inputs = models.JSONField(blank=True, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.template_type}'


class email(TimeStampedModel):
    """Model for email configuration"""
    sender = models.EmailField(blank=True, null=True)
    reference = models.CharField(max_length=200,
                                 help_text='Enter email reference',
                                 unique=True, null=False, blank=False)
    subject = models.ForeignKey(subject, related_name='email_subject',
                                on_delete=models.SET_NULL, blank=True,
                                null=True,
                                help_text="Select Email Subject")
    template_type = models.ForeignKey(template, related_name='email_template',
                                      on_delete=models.SET_NULL,
                                      blank=True, null=True,
                                      help_text="Select Email Template")
    recipients = models.ManyToManyField(recipient,
                                        related_name='email_recipients',
                                        blank=True)

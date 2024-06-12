import logging
from rest_framework import serializers

from .models import (email, recipient, subject, template)

logger = logging.getLogger('dict_config_logger')


class EmailSerializer(serializers.ModelSerializer):
    """Serializer for model Email"""
    recipients = serializers.SlugRelatedField(
        many=True, slug_field='email_address',
        queryset=recipient.objects.all())
    subject = serializers.SlugRelatedField(slug_field='subject',
                                           queryset=subject.objects.all(), )
    template_inputs = serializers.SerializerMethodField('get_template_inputs')

    class Meta:
        model = email
        fields = ['recipients', 'subject', 'template_inputs']

    def get_template_inputs(self, email):
        template_inputs = email.template_type.template_inputs
        return template_inputs


class TemplateSerializer(serializers.ModelSerializer):
    """Serializer for model Template"""
    class Meta:
        model = template
        fields = ['template_type', 'message', 'template_inputs']

    def save(self):
        """Save function to create new templates """

        # # Assigning validated data as dictionary for updates in records
        validated_data = dict(
            list(self.validated_data.items())
        )

        # If value to update is present in metadata ledger
        if self.instance is None:

            self.instance = self.create(validated_data)
        else:
            logger.info("No new templates found for the Team")

        return self.instance

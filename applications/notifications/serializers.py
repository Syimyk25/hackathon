from rest_framework import serializers

from applications.notifications.models import ContactSuv


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactSuv
        fields = '__all__'
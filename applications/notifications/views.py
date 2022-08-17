
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from applications.notifications.models import ContactSuv
from applications.notifications.serializers import ContactSerializer


class ContactSuvView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = ContactSuv.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

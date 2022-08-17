from django.db import models


class ContactSuv(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

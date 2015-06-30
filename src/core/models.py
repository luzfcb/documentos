from django.db import models
from django.utils import timezone
from django.conf import settings

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# basically is this:
class Document(models.Model):
    content = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    created_by = models.ForeignKey(to=USER_MODEL,
                                   related_name="%(app_label)s_%(class)s_created_by", null=True,
                                   blank=True, on_delete=models.SET_NULL)

    modified_at = models.DateField(auto_now=True, blank=True, editable=False)
    modified_by = models.ForeignKey(to=USER_MODEL,
                                    related_name="%(app_label)s_%(class)s_modified_by", null=True,
                                    blank=True, on_delete=models.SET_NULL)

from __future__ import absolute_import, unicode_literals, print_function
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.conf import settings
from model_utils import tracker
from redactor.fields import RedactorField
from .fields import CounterField
import sequence_field
from simple_history.models import HistoricalRecords

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Document(models.Model):
    content_tracker = tracker.FieldTracker()


# basically is this:
class DocumentContent(models.Model):
    conteudo = models.OneToOneField('Document', related_name="conteudo", null=True, on_delete=models.SET_NULL,
                                    editable=False)
    title = models.CharField(blank=True, max_length=500)
    content = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now, blank=True, editable=False)
    created_by = models.ForeignKey(to=USER_MODEL,
                                   related_name="%(app_label)s_%(class)s_created_by", null=True,
                                   blank=True, on_delete=models.SET_NULL)

    modified_at = models.DateField(auto_now=True, blank=True, editable=False)
    modified_by = models.ForeignKey(to=USER_MODEL,
                                    related_name="%(app_label)s_%(class)s_modified_by", null=True,
                                    blank=True, on_delete=models.SET_NULL)

    is_active = models.NullBooleanField(default=True, editable=False)

    content_tracker = tracker.FieldTracker()

    historico_modificacoes = HistoricalRecords()

    # certificacao_digital, pega fields relavantes e gera identificador unico para os dados e bloqueia para edicao

    def __unicode__(self):
        return "{}".format(self.content)

    @property
    def _history_user(self):
        return self.modified_by

    @_history_user.setter
    def _history_user(self, value):
        self.modified_by = value




class Pessoa(models.Model):
    conteudo = models.TextField(blank=True)
    # conteudo = RedactorField(
    #
    #
    #     allow_file_upload=True,
    #     allow_image_upload=True
    # )
    user = models.ForeignKey(to=USER_MODEL, null=True)

    historico_modificacoes = HistoricalRecords()

    # a = models.DateTimeField(auto_now_add=True)
    contador = CounterField()
    contador2 = models.IntegerField(default=0, auto_created=True, editable=False)

    def __unicode__(self):
        return "{} - {} - {} - {}".format(self.conteudo, self.user, self.contador, self.contador2)

    def save(self, *args, **kwargs):
        if self.pk:
            max_db_value = self.historico_modificacoes.aggregate(Max('contador2')).values()[0]
            self.contador2 = max_db_value + 1 if max_db_value >= self.contador2 else self.contador2 + 1
            self.conteudo = "{} - {}".format(self.conteudo, self.contador2)

        super(Pessoa, self).save(*args, **kwargs)


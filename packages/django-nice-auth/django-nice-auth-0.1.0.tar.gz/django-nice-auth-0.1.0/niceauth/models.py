# niceauth/models.py

from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField('Created At', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}({})'.format(self.title, self.id)


class NiceAuthRequest(BaseModel):
    request_no = models.CharField(max_length=30, unique=True)
    enc_data = models.TextField()
    integrity_value = models.TextField()
    token_version_id = models.CharField(max_length=100)
    key = models.CharField(max_length=32)
    iv = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'Nice Auth Request'
        verbose_name_plural = 'Nice Auth Requests'
        ordering = ['-created_at']


class NiceAuthResult(BaseModel):
    request = models.OneToOneField(NiceAuthRequest, on_delete=models.CASCADE)
    result_data = models.JSONField()

    class Meta:
        verbose_name = 'Nice Auth Result'
        verbose_name_plural = 'Nice Auth Results'
        ordering = ['-created_at']

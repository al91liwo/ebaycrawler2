from django.db import models


class EbayUser(models.Model):
    first_name = models.CharField(name='first_name', blank=True, null=False, max_length=20)
    last_name = models.CharField(name='last_name', blank=True, null=False, max_length=20)
    company_name = models.CharField(default='', blank=True, null=False, max_length=100)
    email = models.EmailField(null=False, blank=False, unique=True)
    street = models.CharField(max_length=20, blank=True, null=False)
    plz = models.CharField(max_length=10, blank=True, null=False)
    city = models.CharField(max_length=20, blank=True, null=False)
    date_acquired = models.DateTimeField(auto_now=True)
    date_sent = models.DateTimeField(auto_now=False, null=True, blank=True)
    date_cleaned = models.DateTimeField(auto_now=False, null=True, blank=True)
    description = models.CharField(max_length=3333, blank=True, null=False)
    link = models.URLField(blank=True, null=True)
    cleaned = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class EmailTemplate(models.Model):
    subject = models.CharField(max_length=120, blank=False, null=False)
    text = models.CharField(max_length=5000, blank=False, null=False)


class AttachmentTemplate(models.Model):
    attachment = models.FileField(upload_to='')


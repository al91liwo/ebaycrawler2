from django.contrib import admin
from .models import *


class EbayUserAdmin(admin.ModelAdmin):
    search_fields = ['email']


admin.site.register(EbayUser, EbayUserAdmin)
admin.site.register(EmailTemplate)
admin.site.register(AttachmentTemplate)

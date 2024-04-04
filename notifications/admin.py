from .models import EmailConfig
from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Notifications)
class NotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailConfig)
class EmailConfigAdmin(admin.ModelAdmin):
    list_display = ('from_email', 'email_host',
                    'email_port', 'use_tls', 'fail_silently')
    list_editable = ('email_host', 'email_port', 'use_tls', 'fail_silently')
    search_fields = ('from_email', 'email_host', 'email_port')


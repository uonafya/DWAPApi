from django.db import models

# Create your models here.
class middleware_settings(models.Model):
    syncdata = models.BooleanField(default=False)
    server_url = models.URLField(
        default="https://khis.pmtct.uonbi.ac.ke/api/29/analytics.json&filter=ou:", blank=True, null=True)
    server_username=models.CharField(max_length=255,default='healthit')
    server_password = models.CharField(max_length=255, default="rr23H3@1th1Tmtct")

    def __str__(self):
        return "Sync Settings"

    class Meta:
        verbose_name_plural = 'Sync Settings'

class schedule_settings(models.Model):
    sync_time = models.DateTimeField()
    shedule_description = models.CharField(
        default="Weekely  data sync", max_length=255, blank=True, null=True)

    def __str__(self):
        return "Schedule Settings"

    class Meta:
        verbose_name_plural = 'Schedule Settings'

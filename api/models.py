from operator import mod
from tabnanny import verbose
from django.db import models

# indicators


class indicators(models.Model):
    id = models.CharField(max_length=500, primary_key=True)
    name = models.CharField(max_length=500)
    lastUpdated = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    shortName = models.CharField(max_length=500, blank=True, null=True)
    displayName = models.CharField(max_length=500, blank=True, null=True)
    displayShortName = models.CharField(max_length=500, blank=True, null=True)
    displayNumeratorDescription = models.CharField(
        max_length=500, blank=True, null=True)
    denominatorDescription = models.CharField(
        max_length=500, blank=True, null=True)
    displayDenominatorDescription = models.CharField(
        max_length=500, blank=True, null=True)
    numeratorDescription = models.CharField(
        max_length=500, blank=True, null=True)
    dimensionItem = models.CharField(max_length=500, blank=True, null=True)
    displayFormName = models.CharField(max_length=500, blank=True, null=True)
    numerator = models.CharField(max_length=2500, blank=True, null=True)
    denominator = models.CharField(max_length=2500, blank=True, null=True)
    dimensionItemType = models.CharField(max_length=500, blank=True, null=True)
    indicatorType = models.ForeignKey(
        'indicatorType', on_delete=models.CASCADE, related_name='indicators', blank=True, null=True)
    indicatorGroups = models.ManyToManyField(
        'indicatorGroups', blank=True, null=True)

    def __str__(self):
        return self.displayName

    class Meta:
        db_table = 'moh_indicators'
        verbose_name_plural = 'indicators'


class indicatorType(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'moh_indicator_types'
        verbose_name_plural = 'indicators types'


class indicatorGroups(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    lastUpdated = models.DateTimeField()
    created = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'moh_indicator_groups'
        verbose_name_plural = 'indicators groups'


class middleware_settings(models.Model):
    syncdata = models.BooleanField(default=False)
    client_url = models.URLField(
        default="https://test.hiskenya.org/dhiske/", blank=True, null=True)

    def __str__(self):
        return "Data Sync Settings"

    class Meta:
        db_table = 'middleware_settings'
        verbose_name_plural = 'Data Sync Settings'


class schedule_settings(models.Model):
    sync_time = models.TimeField()
    shedule_description = models.CharField(
        default="Weekely  data sync", max_length=255, blank=True, null=True)
    sync_m = models.IntegerField(default=0)
    sync_t = models.IntegerField(default=0)
    sync_w = models.IntegerField(default=0)
    sync_th = models.IntegerField(default=0)
    sync_f = models.IntegerField(default=0)
    sync_s = models.IntegerField(default=0)
    sync_su = models.IntegerField(default=0)

    def __str__(self):
        return "Schedule Settings"

    class Meta:
        db_table = 'schedule_settings'
        verbose_name_plural = 'Schedule Settings'


class total_records(models.Model):
    records = models.IntegerField(default=0)

    def __str__(self):
        return str(self.records) if self.records is not None or '' else "No Files yet!"

    class Meta:
        db_table = 'khis_total_records'
        verbose_name_plural = 'Total Records'


class Data_Mapping_Files(models.Model):
    file = models.FileField(upload_to='mapping/files/%Y-%m-%d/')
    final_file = models.FileField(
        upload_to='mapping/final/%Y-%m-%d/', blank=True, null=True)

    def __str__(self):
        return self.file.url

    class Meta:
        db_table = 'data_mapping_files'
        verbose_name_plural = 'Data Mapping Files'

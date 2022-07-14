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

from django.db import models
from datetime import datetime
# Create your models here.


class SeriesColumns(models.Model):
    datim_main_comparison_column = models.CharField(
        max_length=255, default='Datim_Disag_Name', help_text='Map indicators to MOH using this column')
    moh_main_comparison_column = models.CharField(
        max_length=255, default='MOH_Indicator_Name', help_text='Map indicators to Datim using this column')
    last_updated = models.DateTimeField(
        auto_now_add=True, null=True)

    class Meta:
        db_table = 'mapping_series_columns'
        verbose_name_plural = 'Dataset Series Columns To Map'

    def __str__(self) -> str:
        return "Defined Columns"


class KeyComparisonElements(models.Model):
    age_group = models.BooleanField(default=True)
    gender = models.BooleanField(default=True)
    similar_words = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'key_comparison_elements'
        verbose_name_plural = 'Key Comparison Elements'

    def __str__(self) -> str:
        return "Comparison Elements"


class SeriesRegex(models.Model):
    age_group_regex = models.CharField(
        max_length=255, default='(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})', help_text="Regex to extract age group")
    gender_regex = models.CharField(
        max_length=1500, default="\((F|M)\)|(Male|Female)", help_text='Regex to extract MOH Gender')
    last_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'series_regex'
        verbose_name_plural = 'Mapping regex definations'

    def __str__(self) -> str:
        return f"{self.age_group_regex} -{self.gender_regex}"


class MiscSettings(models.Model):
    merge_25_plus_ages = models.BooleanField(default=True)
    merge_1_to_9_ages = models.BooleanField(default=True)
    max_word_similarity = models.IntegerField(default=30)
    last_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'misc'
        verbose_name_plural = 'Miscleneous Settings'

    def __str__(self) -> str:
        return str(self.last_updated)


class DatasetColumns_Ranaming(models.Model):
    original_name = models.CharField(
        max_length=500, default='orglevel2', null=True)
    rename_to = models.CharField(
        max_length=255, default="county", help_text='Rename columns to a simpler name', null=True)
    last_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'dataset_column_renaming'
        verbose_name_plural = 'Rename Dataset Columns'

    def __str__(self) -> str:
        return "{} - {}".format(self.original_name, self.rename_to)

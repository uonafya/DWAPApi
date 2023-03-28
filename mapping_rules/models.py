from django.db import models

# Create your models here.


class SeriesColumns(models.Model):
    datim_main_comparison_column = models.CharField(
        max_length=255, default='Datim_Disag_Name', help_text='Map indicators to MOH using this column')
    moh_main_comparison_column = models.CharField(
        max_length=255, default='MOH_Indicator_Name', help_text='Map indicators to Datim using this column')
    datim_cols = models.TextField(
        max_length=1500, default="orgunitlevel2,orgunitlevel2,orgunitlevel3,orgunitlevel4,orgunitlevel5,organisationunitid,dataid,dataname,Oct to Dec 2021,Jan to Mar 2022,Apr to Jun 2022")
    moh_cols = models.TextField(
        max_length=1500, default="MOH_FacilityID,facility,ward,subcounty,county,MOH_IndicatorCode,inndicator,Value,Period")
    datim_moh_columns_to_display = models.TextField(
        max_length=1500, default="MOH_FacilityID,MOH_IndicatorCode,DATIM_Disag_ID,county,subcounty,ward,facility")

    class Meta:
        db_table = 'mapping_series_columns'
        verbose_name_plural = 'Dataset Series Columns To Map'

    def __str__(self) -> str:
        return "Defined Columns"


class SeriesRegex(models.Model):
    regex_name = models.CharField(
        max_length=255, default='Ageset Regex', help_text="Use names related to what the regex does e.g ageset regex for getting ageset")
    regex_pattern = models.CharField(
        max_length=1500, default="(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})", help_text='Load regex as raw using r')

    class Meta:
        db_table = 'series_regex'
        verbose_name_plural = 'Mapping regex definations'

    def __str__(self) -> str:
        return self.regex_name


class GruopSeriesData(models.Model):
    dataset_name = models.CharField(
        max_length=255, default='datim', help_text="Dataset Name")
    group_by = models.CharField(
        max_length=255, default='DATIM_Indicator_Category', help_text="Group dataset by indicator category")

    class Meta:
        db_table = 'series_groups'
        verbose_name_plural = 'Series Data Grouping'

    def __str__(self) -> str:
        return self.dataset_name


class DatasetColumns_Ranaming(models.Model):
    dataset_name = models.CharField(
        max_length=255, default='datim', help_text="Dataset Name")
    original_name = models.CharField(
        max_length=500, default='orglevel2', null=True)
    rename_to = models.CharField(
        max_length=255, default="county", help_text='Rename columns to a simpler name', null=True)

    class Meta:
        db_table = 'dataset_column_renaming'
        verbose_name_plural = 'Rename Dataset Columns'

    def __str__(self) -> str:
        return "{} - {}".format(self.original_name, self.rename_to)

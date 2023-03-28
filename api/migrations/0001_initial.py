# Generated by Django 4.1.7 on 2023-03-22 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='counties',
            fields=[
                ('county_name', models.CharField(max_length=500, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Counties',
                'db_table': 'counties',
            },
        ),
        migrations.CreateModel(
            name='Data_Mapping_Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mapping_files', models.FileField(upload_to='mapping_files/')),
                ('final_mapped', models.FileField(blank=True, null=True, upload_to='final_mapped/')),
                ('final_comparison', models.FileField(blank=True, null=True, upload_to='final_comparison/')),
            ],
            options={
                'verbose_name_plural': 'Data Mapping Files',
                'db_table': 'data_mapping_files',
            },
        ),
        migrations.CreateModel(
            name='final_comparison_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(blank=True, null=True)),
                ('facility', models.CharField(blank=True, max_length=500, null=True)),
                ('ward', models.CharField(blank=True, max_length=500, null=True)),
                ('subcounty', models.CharField(blank=True, max_length=500, null=True)),
                ('county', models.CharField(blank=True, max_length=255, null=True)),
                ('MOH_FacilityID', models.CharField(blank=True, max_length=500, null=True)),
                ('DATIM_Disag_ID', models.CharField(blank=True, max_length=500, null=True)),
                ('MOH_IndicatorCode', models.CharField(blank=True, max_length=500, null=True)),
                ('indicators', models.CharField(blank=True, max_length=1500, null=True)),
                ('category', models.CharField(blank=True, max_length=1500, null=True)),
                ('DATIM_Disag_Name', models.CharField(blank=True, max_length=1500, null=True)),
                ('khis_data', models.CharField(blank=True, max_length=255, null=True)),
                ('datim_data', models.CharField(blank=True, max_length=255, null=True)),
                ('weight', models.FloatField(blank=True, max_length=255, null=True)),
                ('concodance', models.FloatField(blank=True, max_length=255, null=True)),
                ('khis_minus_datim', models.IntegerField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Fianl Comparison Data',
                'db_table': 'final_comparison_data',
            },
        ),
        migrations.CreateModel(
            name='indicator_category',
            fields=[
                ('category_name', models.CharField(max_length=500, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Indicator Categories',
                'db_table': 'indicator_category',
            },
        ),
        migrations.CreateModel(
            name='indicatorGroups',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('lastUpdated', models.DateTimeField()),
                ('created', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'indicators groups',
                'db_table': 'moh_indicator_groups',
            },
        ),
        migrations.CreateModel(
            name='indicatorType',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'indicators types',
                'db_table': 'moh_indicator_types',
            },
        ),
        migrations.CreateModel(
            name='mapped_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_Mapped', models.DateTimeField(auto_now_add=True, null=True)),
                ('DATIM_Indicator_Category', models.CharField(blank=True, max_length=255, null=True)),
                ('DATIM_Indicator_ID', models.CharField(blank=True, max_length=500, null=True)),
                ('DATIM_Disag_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('DATIM_Disag_ID', models.CharField(blank=True, max_length=255, null=True)),
                ('Operation', models.CharField(blank=True, max_length=20, null=True)),
                ('MOH_Indicator_Name', models.CharField(blank=True, max_length=1500, null=True)),
                ('MOH_Indicator_ID', models.CharField(blank=True, max_length=500, null=True)),
                ('Disaggregation_Type', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Mapped Data',
            },
        ),
        migrations.CreateModel(
            name='middleware_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('syncdata', models.BooleanField(default=False)),
                ('client_url', models.URLField(blank=True, default='https://test.hiskenya.org/dhiske/', null=True)),
            ],
            options={
                'verbose_name_plural': 'Data Sync Settings',
                'db_table': 'middleware_settings',
            },
        ),
        migrations.CreateModel(
            name='schedule_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sync_time', models.DateTimeField()),
                ('shedule_description', models.CharField(blank=True, default='Weekely  data sync', max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Schedule Settings',
                'db_table': 'schedule_settings',
            },
        ),
        migrations.CreateModel(
            name='total_records',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('records', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Total Records',
                'db_table': 'khis_total_records',
            },
        ),
        migrations.CreateModel(
            name='indicators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.CharField(blank=True, max_length=500, null=True)),
                ('ward', models.CharField(blank=True, max_length=500, null=True)),
                ('subcounty', models.CharField(blank=True, max_length=500, null=True)),
                ('county', models.CharField(blank=True, max_length=500, null=True)),
                ('MOH_UID', models.CharField(blank=True, max_length=255, null=True)),
                ('MOH_Indicator_ID', models.CharField(max_length=500)),
                ('MOH_Indicator_Name', models.CharField(blank=True, max_length=500, null=True)),
                ('lastUpdated', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('shortName', models.CharField(blank=True, max_length=500, null=True)),
                ('displayName', models.CharField(blank=True, max_length=500, null=True)),
                ('displayShortName', models.CharField(blank=True, max_length=500, null=True)),
                ('displayNumeratorDescription', models.CharField(blank=True, max_length=500, null=True)),
                ('denominatorDescription', models.CharField(blank=True, max_length=500, null=True)),
                ('displayDenominatorDescription', models.CharField(blank=True, max_length=500, null=True)),
                ('numeratorDescription', models.CharField(blank=True, max_length=500, null=True)),
                ('dimensionItem', models.CharField(blank=True, max_length=500, null=True)),
                ('displayFormName', models.CharField(blank=True, max_length=500, null=True)),
                ('numerator', models.CharField(blank=True, max_length=2500, null=True)),
                ('denominator', models.CharField(blank=True, max_length=2500, null=True)),
                ('dimensionItemType', models.CharField(blank=True, max_length=500, null=True)),
                ('khis_data', models.CharField(blank=True, max_length=255, null=True)),
                ('indicatorGroups', models.ManyToManyField(blank=True, null=True, to='api.indicatorgroups')),
                ('indicatorType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='indicators', to='api.indicatortype')),
            ],
            options={
                'verbose_name_plural': 'indicators',
                'db_table': 'moh_indicators',
            },
        ),
    ]

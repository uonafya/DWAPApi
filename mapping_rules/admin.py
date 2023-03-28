from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([SeriesColumns, SeriesRegex,
                    GruopSeriesData, DatasetColumns_Ranaming])

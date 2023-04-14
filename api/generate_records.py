from .load_files import *
from .models import *
from datetime import datetime, timedelta, date
from django.db.models import Q
from .map_data import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics


@api_view()
def load_filter_data(request):
    mapping_df = load_mapping_csv("all", "all")
    # print(mapping_df)
    datim_df = get_datim_non_null_values("all", "all", "2022-10-01")
    print(datim_df)
    for item in mapping_df.DATIM_Indicator_Category.unique():
        cats, created = indicator_category.objects.get_or_create(
            category_name=item)
    for item in datim_df.county.unique():
        countie, created = counties.objects.get_or_create(county_name=item)
    return Response({"Operation succeeded...Counties and Indicator Categories in dataset loaded successfully!"})


@ api_view()
def generate_comparison_file(request, data_source, category, county, from_date, to_date):
    # try:
    # import pdb
    # print(data_source, county)
    datim_df = get_datim_non_null_values(category, county, from_date)
    moh_df = get_moh_non_null_values(county)
    # print(datim_df['created'].iloc[0], from_date, to_date)
    if datim_df.empty:
        return Response({"message": "Could not find datim file for the selected indicator!\nPlease upload the file under the \'Uploads Files\' tab"})
    mohdict = {}
    datimdict = {}
    datim_df['created'] = pd.to_datetime(
        datim_df['created'], format='%Y-%m-%d')
    # print(data_source, datim_df)
    if int(datim_df.created.iloc[0].month) == 10:
        from_date = from_date - timedelta(days=365)
        to_date = to_date - timedelta(days=365)
    # Filter data between two dates
    mask = (datim_df['created'] >= pd.to_datetime(from_date)) & (
        datim_df['created'] <= pd.to_datetime(to_date))
    datim_df = datim_df.loc[mask]
    if str(data_source).lower() == 'api data':
        datimdict = datim_df.to_dict(orient='records')
        objects = indicators.objects.filter(Q(MOH_Indicator_Name__icontains='MOH 731'), created__range=[
            from_date, to_date]).order_by('-created')
        mohdict = list(objects.values())
    else:
        datimdict = datim_df.to_dict(orient='records')
        # print(datimdict[0])
        moh_df['created'] = pd.to_datetime(
            moh_df['created'], format='%Y-%m-%d')
        mask = (moh_df['created'] >= pd.to_datetime(from_date)) & (
            moh_df['created'] <= pd.to_datetime(to_date))
        # Filter data between two dates
        moh_df = moh_df.loc[mask]
        moh_df.iloc[:datim_df.shape[0]]
        print(moh_df.info())
        mohdict = moh_df.to_dict(orient='records')
        # pdb.set_trace()
    if len(mohdict) == 0:
        return Response({"message": "Could not find data to process!"})
    if len(datimdict) == 0:
        return Response({"message": "Could not find data to process!"})
    temp_df = map_data(mohdict, datimdict)
    if temp_df.empty:
        return Response({"message": "Could not find any match for the dataset supplied!"})
    temp_df['weight'] = temp_df.datim_data/temp_df.datim_data.sum()
    # calculate concodance
    temp_df['concodance(%)'] = (temp_df['weight']*100*(((temp_df['khis_data']+temp_df['datim_data']) -
                                                        abs(temp_df['khis_data']-temp_df['datim_data']))/(temp_df['khis_data']+temp_df['datim_data'])))
    temp_df['khis_minus_datim'] = temp_df['khis_data'] - \
        temp_df['datim_data']
    final_dict = temp_df.to_dict(orient='records')
    # print(temp_df.columns)
    for record in final_dict:
        final_data, created = final_comparison_data.objects.get_or_create(
            create_date=pd.to_datetime(record['created']).date(),
            facility=record['facility'],
            ward=record['ward'],
            subcounty=record['subcounty'],
            county=record['county'],
            MOH_FacilityID=record['MOH_FacilityID'],
            category=record['category'],
            DATIM_Disag_ID=record['DATIM_Disag_ID'],
            MOH_IndicatorCode=record['MOH_IndicatorCode'],
            indicators=record['MOH_Indicator_Name'],
            DATIM_Disag_Name=record['DATIM_Disag_Name'],
            khis_data=record['khis_data'],
            datim_data=record['datim_data'],
            weight=record['weight'],
            concodance=record['concodance(%)'],
            khis_minus_datim=record['khis_minus_datim'])
        final_mapped_data, created = mapped_data.objects.get_or_create(DATIM_Indicator_Category=str(
            record['category']), DATIM_Disag_ID=str(record['DATIM_Disag_ID']), DATIM_Disag_Name=str(record['DATIM_Disag_Name']),
            MOH_Indicator_Name=str(record['MOH_Indicator_Name']), MOH_Indicator_ID=str(record['MOH_IndicatorCode']),
            Disaggregation_Type=str('Coarse'))
        # print(final_data)
        # print(final_mapped_data)
    temp_df.to_csv(os.path.join(os.path.join(ABSOLUTE_PATH(), 'media\\final_mapped'),
                                'Final_Datim_Mapped_Csv_File'+str(datetime.now().minute)+".csv"), index=False)
    print(temp_df['concodance(%)'].sum())
    print(final_data)
    return Response({"message": "Data Comparison mapping for {} completed successfully!".format(str(county))})
    # except Exception as e:
    #     print("mapping error:{}".format(e))
    #     return Response({"error": str(e)})


class GetMappedFiles(generics.ListAPIView):
    serializer_class = mappedDataSerializer
    permission_classes = ()

    def get_queryset(self):
        return mapped_data.objects.all()

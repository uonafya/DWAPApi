from .load_files import *
from .models import *
from datetime import datetime
from .comparedata import *


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


# @api_view()
# def map_data(request, county, category, from_date, to_date, limit):
#     datim_df = get_datim_non_null_values(category, county, from_date)
#     datimdict = datim_df.to_dict(orient='records')
#     moh_df = get_moh_non_null_values(county)
#     mohdict = []
#     moh_csv_dict = moh_df.to_dict(orient='records')
#     gender = ''
#     dageset = 0
#     datimageset = ''
#     ageset = ''
#     mageset = 0
#     found = False
#     temp_dict = []
#     # add moh data
#     # try:
#     #     for item in moh_csv_dict:
#     #         mohdata, created = indicators.objects.get_or_create(facility=item['facility'], ward=item['ward'], subcounty=item['subcounty'], county=item[
#     #                                                             'county'],    MOH_UID=item['MOH_UID'], MOH_Indicator_ID=item['MOH_Indicator_ID'], MOH_Indicator_Name=item['MOH_Indicator_Name'], lastUpdated=timezone.now(), created=timezone.now(), khis_data=item['khis_data'])
#     #     print(mohdata[0])
#     # except Exception as e:
#     #     print(e)
#     objects = indicators.objects.filter(
#         Q(MOH_Indicator_Name__icontains='MOH 731')).order_by('-created')
#     mohdict = list(objects.values())
#     # print(mohdict[0])
#     # try:
#     for i, m in enumerate(mohdict):
#         for j, d in enumerate(datimdict):
#             dk0 = d['DATIM_Disag_Name'].replace('|', '').replace('|', '')
#             mk0 = m['MOH_Indicator_Name'].replace('_', ' ').replace('(', ' (')
#             # print(mk0)
#             # print(dk0)
#             # DATIM ageset
#             pattern = "(\d+)"
#             dageset = int(get_regex_value(pattern, dk0))
#             if datimageset != None or '':
#                 check_datim_ageset = ""
#                 if re.search("[-]", datimageset) != None:
#                     dageset = int(datimageset.split('-')[1])
#                 elif re.search("[+]", datimageset) != None:
#                     dageset = int(datimageset.strip("+"))
#                 else:
#                     dageset = int(datimageset.strip('<'))
#                 # map to <15
#                 if dageset == 1:
#                     dk0 = dk0.replace(datimageset, "<15")
#                     check_datim_ageset = "<1"
#                 elif dageset > 1 and dageset <= 9:
#                     dk0 = dk0.replace(datimageset, "<15")
#                     check_datim_ageset = "1-9"
#                 elif dageset > 9 and dageset <= 14:  # <15
#                     dk0 = dk0.replace(datimageset, "<15")
#                     check_datim_ageset = "10-14"
#                 # map to 15+
#                 if dageset > 15 and dageset <= 19:  # 15+
#                     dk0 = dk0.replace(datimageset, "15+")
#                     check_datim_ageset = "15-19"
#                 elif dageset > 19 and dageset <= 24:  # 15+
#                     dk0 = dk0.replace(datimageset, "15+")
#                     check_datim_ageset = "20-24"
#                 if dageset >= 25:  # 15+
#                     dk0 = dk0.replace(datimageset, "15+")
#                     datim_25_plus = 25
#             # print(dageset)
#             # MOH ageset
#             pattern = r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})"
#             moh_ageset = get_regex_value(pattern, mk0)
#             ageset = get_regex_value(pattern, mk0)
#             mageset = int(ageset.strip('+').strip('<').split('-')[0])
#             # print(ageset)
#             # check gender
#             if re.search("[r'('][F][r')']", mk0) != None:
#                 gender = 'Female'
#             elif re.search("[r'('][M][r')']", mk0) != None:
#                 gender = 'Male'
#             else:
#                 gender = 'Unknown Sex'
#             # print(gender)
#             if re.search('Completed IPT_12months', m['MOH_Indicator_Name']) != None and 'TB_PREV' in d['DATIM_Indicator_Category']:
#                 if re.search("([<]|[+]", dk0) != None and re.search('(Female|Male|Unknown Sex)', dk0) != None and re.search('(Newly Enrolled|Previously Enrolled)', dk0) != None:
#                     # print("{}\t<= Completed IPT_12months =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
#                     found = True
#                     append_data(temp_dict, m, d)
#                     datimdict.remove(datimdict[j])
#                     break
#             else:
#                 if (d['DATIM_Indicator_Category'] == 'TX_CURR'):
#                     # <15 M|F
#                     if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
#                         # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # <15 1-9|<1 unknown sex
#                     elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
#                         # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # 15+ M|F
#                     elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
#                         # print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(m['facility'],j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                 elif (d['DATIM_Indicator_Category'] == 'HTS_TST'):
#                     # <15 Positive M|F
#                     if get_regex_value("((Positive)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", dk0) != None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
#                         # print("{}\t<= positive to positive mapping ageles =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # <15 Positive Unknown Sex
#                     elif get_regex_value("((Positive)\s+[<](\d+)\s+(\w+)\s+(\w+))") != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # 15+ Positive M|F
#                     elif get_regex_value("((Positive)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
#                         # print("{}\t<= positive to positive mapping ageplus =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # <15 Negative M|F Positive
#                     elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
#                         # print("{}\t<= negative to pstve|tested ageless sub =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # <15 Negative M|F Tested
#                     elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
#                         # print("{}\t<= negative to pstve|tested ageless add  =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # <15 Negative|Positive  Unknown Sex
#                     elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # <15 Negative|Tested  Unknown Sex
#                     elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None:
#                         # print("{}\t<= negative to pstve|tested mapping ageless sex unknown =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # 15+ Negative M|F Positive
#                     elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # 15+ Negative M|F Tested
#                     elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Tested", mk0).group() != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                 elif (d['DATIM_Indicator_Category'] == 'PMTCT_ART') and re.search("Total", dk0) != None:
#                     if re.search("On HAART at 1st ANC", m['MOH_Indicator_Name']) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     elif re.search("Start HAART_ANC", m['MOH_Indicator_Name']) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                 elif (d['DATIM_Indicator_Category'] == 'PMTCT_STAT'):
#                     if get_regex_value("((Known)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Known Positive at 1st  ANC", m['MOH_Indicator_Name']) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     elif get_regex_value("((Newly)\s+(\w+)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Positive Results_ANC", m['MOH_Indicator_Name']) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     elif re.search("((New)\s+(\w+)\s+(\w+))", dk0) != None and re.match("Initial test at ANC", m['MOH_Indicator_Name']) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     elif re.search("((New)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Positive Results_ANC", m['MOH_Indicator_Name']) != None:
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                 elif (d['DATIM_Indicator_Category'] == 'TX_NEW'):
#                     # <15 M|F
#                     if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
#                         # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # <15 1-9|<1 unknown sex
#                     elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
#                         # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#                     # 15+ M|F
#                     elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
#                         # print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(m['facility'],j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
#                         found = True
#                         append_data(temp_dict, m, d)
#                         datimdict.remove(datimdict[j])
#                         break
#         if found:
#             continue
#     # print(temp_dict)
#     temp_df = pd.DataFrame(temp_dict)
#     temp_df.drop_duplicates(inplace=True)
#     # print(temp_df)
#     temp_df.info()
#     # NaN_df = get_NaN_Values()
#     # final_df = temp_df.append(NaN_df, ignore_index=True)
#     # print(temp_df.tail(2))
#     final_dict = temp_df.to_dict(orient='records')
#     # print(final_dict)
#     for i, j in enumerate(final_dict):
#         final_data, created = mapped_data.objects.get_or_create(DATIM_Indicator_Category=str(
#             j['DATIM_Indicator_Category']), DATIM_Indicator_ID=str(j['DATIM_Indicator_ID']), DATIM_Disag_ID=str(j['DATIM_Disag_ID']), DATIM_Disag_Name=str(j['DATIM_Disag_Name']), Operation=str(j['Operation']), MOH_Indicator_Name=str(j['MOH_Indicator_Name']), MOH_Indicator_ID=str(j['MOH_Indicator_ID']), Disaggregation_Type=str(j['Disaggregation Type']))
#         print(final_data)
#     temp_df.to_csv(os.path.join(os.path.join(ABSOLUTE_PATH(), 'media\\final_mapped'),
#                                 'Final_Datim_Mapped_Csv_File'+str(datetime.now().minute)+".csv"), index=False)
#     return Response({"Success": "Data Mapping completed successfully!"})
#     # except Exception as e:
#     #     print("mapping error:{}".format(e))
#     #     return Response({"Mapping Error": str(e)})

@ api_view()
def generate_comparison_file(request, use_api_data, category, county, from_date, to_date):
    # try:
    # import pdb
    datim_df = get_datim_non_null_values(category, county, from_date)
    if datim_df.empty:
        return Response({"message": "Could not find datim file for the selected indicator!\nPlease upload the file under the \'Uploads Files\' tab"})
    mohdict = {}
    datimdict = {}
    datim_df['created'] = pd.to_datetime(
        datim_df['created'], format='%Y-%m-%d')
    # Filter data between two dates
    datim_df = datim_df.loc[(datim_df['created'] >= str(
        from_date)) & (datim_df['created'] <= str(to_date))]
    if str(use_api_data).lower() == 'api data':
        datimdict = datim_df.to_dict(orient='records')
        objects = indicators.objects.filter(Q(MOH_Indicator_Name__icontains='MOH 731'), created__range=[
            from_date, to_date]).order_by('-created')
        mohdict = list(objects.values())
    else:
        datimdict = datim_df.to_dict(orient='records')
        print(datim_df.info())
        moh_df = get_moh_non_null_values(county)
        moh_df['created'] = pd.to_datetime(
            moh_df['created'], format='%Y-%m-%d')
        # Filter data between two dates
        moh_df = moh_df.loc[(moh_df['created'] >= str(
            from_date)) & (moh_df['created'] <= str(to_date))]
        moh_df.iloc[:datim_df.shape[0]]
        print(moh_df.info())
        mohdict = moh_df.to_dict(orient='records')
        # pdb.set_trace()
    if len(mohdict) == 0:
        return Response({"message": "Could not find data to process!"})
    if len(datimdict) == 0:
        return Response({"message": "Could not find data to process!"})
    temp_df = compare_data(mohdict, datimdict)
    if temp_df.empty:
        return Response({"message": "Could not find any match for the dataset supplied!"})
    temp_df['weight'] = temp_df.datim_data/temp_df.datim_data.sum()
    # calculate concodance
    temp_df['concodance(%)'] = (temp_df['weight']*100*(((temp_df['khis_data']+temp_df['datim_data']) -
                                                        abs(temp_df['khis_data']-temp_df['datim_data']))/(temp_df['khis_data']+temp_df['datim_data'])))
    temp_df['khis_minus_datim'] = temp_df['khis_data'] - \
        temp_df['datim_data']
    final_dict = temp_df.to_dict(orient='records')
    for record in final_dict:
        final_data, created = final_comparison_data.objects.get_or_create(
            created=pd.to_datetime(record['created']).date(),
            facility=record['facility'],
            ward=record['ward'],
            subcounty=record['subcounty'],
            county=record['county'],
            MOH_FacilityID=record['MOH_FacilityID'],
            category=record['category'],
            DATIM_Disag_ID=record['DATIM_Disag_ID'],
            MOH_IndicatorCode=record['MOH_IndicatorCode'],
            indicators=record['indicators'],
            DATIM_Disag_Name=record['DATIM_Disag_Name'],
            khis_data=record['khis_data'],
            datim_data=record['datim_data'],
            weight=record['weight'],
            concodance=record['concodance(%)'],
            khis_minus_datim=record['khis_minus_datim'])
        final_mapped_data, created = mapped_data.objects.get_or_create(DATIM_Indicator_Category=str(
            record['category']), DATIM_Disag_ID=str(record['DATIM_Disag_ID']), DATIM_Disag_Name=str(record['DATIM_Disag_Name']),
            MOH_Indicator_Name=str(record['indicators']), MOH_Indicator_ID=str(record['MOH_IndicatorCode']),
            Disaggregation_Type=str('Coarse'))
        print(final_data)
        print(final_mapped_data)
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

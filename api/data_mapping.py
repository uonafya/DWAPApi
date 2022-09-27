import pandas as pd
import re
import os
import glob
import re
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions, authentication
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from pathlib import Path
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from .models import *


def ABSOLUTE_PATH():
    return Path(__file__).resolve().parent.parent


def load_mapping_csv(category, county):
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping_files")
    # print(MEDIA_ROOT)
    folder_path = MEDIA_ROOT
    res = []
    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    print(res)
    mapping = os.path.join(
        folder_path,  [i for i in res if re.search('indicatorMapping', i) != None][0])
    # print(datimfile)
    mapping_df = pd.read_csv(
        mapping, usecols=['DATIM_Indicator_Category', 'DATIM_Indicator_ID', 'DATIM_Disag_ID', 'Operation', 'Disaggregation Type'])
    if str(category).lower() != "all":
        mapping_df = mapping_df.query(
            'DATIM_Indicator_Category == "{}"'.format(category))
    else:
        pass
    mapping_df.drop_duplicates(inplace=True)
    return mapping_df


def load_datim_csv(category, county):
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping_files")
    # print(MEDIA_ROOT)
    folder_path = MEDIA_ROOT
    res = []
    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    print(res)
    datimfile = os.path.join(
        folder_path,  [i for i in res if re.search('datim', str(i).lower()) != None][0])
    datim_df = pd.read_csv(datimfile)
    # UID Mappings
    datim_cats = pd.merge(load_mapping_csv(category, county), datim_df,
                          on='DATIM_Disag_ID', how='inner')
    datim_df = datim_cats
    datim_df.rename(columns={'Datim_Facility_UID': 'DATIM_UID'}, inplace=True)
    if str(county).lower() != 'all' and str(category) != 'all':
        datim_df = datim_df.query(
            'DATIM_Indicator_Category == "{}" and county == "{}"'.format(category, county))
    else:
        pass
    datim_df.drop_duplicates(inplace=True)
    return datim_df


def load_moh_csv(county):
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping_files")

    # print(MEDIA_ROOT)
    folder_path1 = MEDIA_ROOT
    res1 = []
    for path1 in os.listdir(folder_path1):
        if os.path.isfile(os.path.join(folder_path1, path1)):
            res1.append(path1)
    print(res1)
    mohfile = os.path.join(
        folder_path1, [i for i in res1 if re.search('khis', i) != None][0])
    moh_df = pd.read_csv(mohfile)
    moh_df.rename(columns={'MOH_Facility_UID': 'MOH_UID'}, inplace=True)
    if str(county).lower() != 'all':
        moh_df = moh_df.query('county == "{}"'.format(county))
    else:
        pass
    moh_df.drop_duplicates(inplace=True)
    return moh_df


def load_mfl_csv():
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping_files")

    # print(MEDIA_ROOT)
    folder_path1 = MEDIA_ROOT
    res1 = []
    for path1 in os.listdir(folder_path1):
        if os.path.isfile(os.path.join(folder_path1, path1)):
            res1.append(path1)
    print(res1)
    mflfile = os.path.join(
        folder_path1, [i for i in res1 if re.search('mfl', str(i).lower()) != None][0])
    mfl_df = pd.read_csv(mflfile)
    return mfl_df


def get_datim_NaN_Values():
    datim_df = load_datim_csv()
    NaN_Values_df = datim_df[datim_df['DATIM_Disag_ID'].isnull()]
    return NaN_Values_df


def get_datim_non_null_values(category, county):
    datim_df = load_datim_csv(category, county)
    datim_df = datim_df[~datim_df['DATIM_Disag_ID'].isnull()]
    datim_df['datim_data'].fillna(0, inplace=True)  # Fill NaN values
    datim_df['datim_data'] = datim_df['datim_data'].astype(int)
    datim_df.drop_duplicates(inplace=True)
    datim_df['created'] = (
        datetime.now()-timedelta(weeks=48, days=30)).date()
    return datim_df


def get_moh_non_null_values(county):
    moh_df = load_moh_csv(county)
    moh_df = moh_df[~moh_df['MOH_Indicator_ID'].isnull()]
    moh_df['khis_data'].fillna(0, inplace=True)  # Fill NaN values
    moh_df['khis_data'] = moh_df['khis_data'].astype(int)
    moh_df.drop_duplicates(inplace=True)
    moh_df['created'] = (
        datetime.now()-timedelta(weeks=48, days=30)).date()
    return moh_df


def append_data(mydict, m, d, check=1):
    if check == 1:
        mydict.append({
            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
            'Operation': d['Operation'],
            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
            'Disaggregation Type': d['Disaggregation Type'],
        })
    else:
        mydict.append({
            'facility': m['facility'],
            'ward': m['ward'],
            'subcounty': m['subcounty'],
            'county': m['county'],
            'MOH_FacilityID': m['MOH_UID'],
            'MOH_IndicatorCode': m['MOH_Indicator_ID'],
            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
            'indicators':  m['MOH_Indicator_Name'],
            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
            'khis_data': m['khis_data'],
            'datim_data': d['datim_data'],
        })


def get_regex_value(pattern, s):
    try:
        x = re.search(pattern, s).group()
        return x
    except Exception as e:
        pass


@api_view()
def load_filter_data(request):
    mapping_df = load_mapping_csv("all", "all")
    datim_df = get_datim_non_null_values("all", "all")
    for item in mapping_df.DATIM_Indicator_Category.unique():
        cats, created = indicator_category.objects.get_or_create(
            category_name=item)
    for item in datim_df.county.unique():
        countie, created = counties.objects.get_or_create(county_name=item)


@api_view()
def map_data(request, county, category):
    datim_df = get_datim_non_null_values(category, county)
    datimdict = datim_df.to_dict(orient='records')
    moh_df = get_moh_non_null_values(county)
    mohdict = []
    moh_csv_dict = moh_df.to_dict(orient='records')
    gender = ''
    dageset = 0
    ageset = ''
    mageset = 0
    found = False
    temp_dict = []
    # add moh data
    # try:
    #     for item in moh_csv_dict:
    #         mohdata, created = indicators.objects.get_or_create(facility=item['facility'], ward=item['ward'], subcounty=item['subcounty'], county=item[
    #                                                             'county'],    MOH_UID=item['MOH_UID'], MOH_Indicator_ID=item['MOH_Indicator_ID'], MOH_Indicator_Name=item['MOH_Indicator_Name'],lastUpdated=timezone.now(),created=timezone.now(), khis_data=item['khis_data'])
    #     print(mohdata[0])
    # except Exception as e:
    #     print(e)
    objects = indicators.objects.filter(
        Q(MOH_Indicator_Name__icontains='MOH 731')).order_by('-created')
    mohdict = list(objects.values())
    print(mohdict[0])
    # try:
    for i, m in enumerate(mohdict):
        for j, d in enumerate(datimdict):
            dk0 = d['DATIM_Disag_Name'].replace('|', '').replace('|', '')
            mk0 = m['MOH_Indicator_Name'].replace('_', ' ').replace('(', ' (')
            # print(mk0)
            # print(dk0)
            # DATIM ageset
            pattern = "(\d+)"
            dageset = int(get_regex_value(pattern, dk0))
            # print(dageset)
            # MOH ageset
            pattern = r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})"
            moh_ageset = get_regex_value(pattern, mk0)
            ageset = get_regex_value(pattern, mk0)
            mageset = int(ageset.strip('+').strip('<').split('-')[0])
            # print(ageset)
            # check gender
            if re.search("[r'('][F][r')']", mk0) != None:
                gender = 'Female'
            elif re.search("[r'('][M][r')']", mk0) != None:
                gender = 'Male'
            else:
                gender = 'Unknown Sex'
            # print(gender)
            if re.search('Completed IPT_12months', m['MOH_Indicator_Name']) != None and 'TB_PREV' in d['DATIM_Indicator_Category']:
                if re.search("([<]|[+]", dk0) != None and re.search('(Female|Male|Unknown Sex)', dk0) != None and re.search('(Newly Enrolled|Previously Enrolled)', dk0) != None:
                    #print("{}\t<= Completed IPT_12months =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                    found = True
                    append_data(temp_dict, m, d)
                    datimdict.remove(datimdict[j])
                    break
            else:
                if (d['DATIM_Indicator_Category'] == 'TX_CURR'):
                    # <15 M|F
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None:
                        #print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None:
                        #print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    #15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        #print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(m['facility'],j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'HTS_TST'):
                    # <15 Positive M|F
                    if get_regex_value("((Positive)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", dk0) != None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        #print("{}\t<= positive to positive mapping ageles =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Positive Unknown Sex
                    elif get_regex_value("((Positive)\s+[<](\d+)\s+(\w+)\s+(\w+))") != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # 15+ Positive M|F
                    elif get_regex_value("((Positive)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        #print("{}\t<= positive to positive mapping ageplus =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Negative M|F Positive
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(ageset, mk0) != None and (mageset < dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        #print("{}\t<= negative to pstve|tested ageless sub =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Negative M|F Tested
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.search(ageset, mk0) != None and (mageset < dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        #print("{}\t<= negative to pstve|tested ageless add  =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Negative|Positive  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(ageset, mk0) != None and (mageset < dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Negative|Tested  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.search(ageset, mk0) != None and (mageset < dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None:
                        #print("{}\t<= negative to pstve|tested mapping ageless sex unknown =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # 15+ Negative M|F Positive
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # 15+ Negative M|F Tested
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Tested", mk0).group() != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'PMTCT_ART') and re.search("Total", dk0) != None:
                    if re.search("On HAART at 1st ANC", m['MOH_Indicator_Name']) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    elif re.search("Start HAART_ANC", m['MOH_Indicator_Name']) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'PMTCT_STAT'):
                    if get_regex_value("((Known)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Known Positive at 1st  ANC", m['MOH_Indicator_Name']) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    elif get_regex_value("((Newly)\s+(\w+)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Positive Results_ANC", m['MOH_Indicator_Name']) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    elif re.search("((New)\s+(\w+)\s+(\w+))", dk0) != None and re.match("Initial test at ANC", m['MOH_Indicator_Name']) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    elif re.search("((New)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Positive Results_ANC", m['MOH_Indicator_Name']) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'TX_NEW'):
                    # <15 M|F
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None:
                        #print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None:
                        #print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    #15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        #print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(m['facility'],j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
        if found:
            continue
    # print(temp_dict)
    temp_df = pd.DataFrame(temp_dict)
    temp_df.drop_duplicates(inplace=True)
    # print(temp_df)
    temp_df.info()
    # NaN_df = get_NaN_Values()
    # final_df = temp_df.append(NaN_df, ignore_index=True)
    # print(temp_df.tail(2))
    final_dict = temp_df.to_dict(orient='records')
    # print(final_dict)
    for i, j in enumerate(final_dict):
        final_data, created = mapped_data.objects.get_or_create(DATIM_Indicator_Category=str(
            j['DATIM_Indicator_Category']), DATIM_Indicator_ID=str(j['DATIM_Indicator_ID']), DATIM_Disag_ID=str(j['DATIM_Disag_ID']), DATIM_Disag_Name=str(j['DATIM_Disag_Name']), Operation=str(j['Operation']), MOH_Indicator_Name=str(j['MOH_Indicator_Name']), MOH_Indicator_ID=str(j['MOH_Indicator_ID']), Disaggregation_Type=str(j['Disaggregation Type']))
        print(final_data)
    temp_df.to_csv(os.path.join(os.path.join(ABSOLUTE_PATH(), 'media\\final_mapped'),
                                'Final_Datim_Mapped_Csv_File.csv'), index=False)
    return Response({"Success": "Data Mapping completed successfully!"})
    # except Exception as e:
    #     print("mapping error:{}".format(e))
    #     return Response({"Mapping Error": str(e)})


def compare_data(mohdict, datimydict):
    gender = ''
    dageset = 0
    ageset = ''
    mageset = 0
    found = False
    temp_dict = []
    # print(mohdict[0])
    # try:
    for i, m in enumerate(mohdict):
        for j, d in enumerate(datimydict):
            dk0 = d['DATIM_Disag_Name'].replace('|', '').replace('|', '')
            mk0 = m['MOH_Indicator_Name'].replace('_', ' ').replace('(', ' (')
            # print(mk0)
            # print(dk0)
            # DATIM ageset
            pattern = "(\d+)"
            dageset = int(get_regex_value(pattern, dk0))
            # print(dageset)
            # MOH ageset
            pattern = r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})"
            moh_ageset = get_regex_value(pattern, mk0)
            ageset = get_regex_value(pattern, mk0)
            mageset = int(ageset.strip('+').strip('<').split('-')[0])
            # print(ageset)
            # check gender
            if re.search("[r'('][F][r')']", mk0) != None:
                gender = 'Female'
            elif re.search("[r'('][M][r')']", mk0) != None:
                gender = 'Male'
            else:
                gender = 'Unknown Sex'
            # print(gender)
            if re.search('Completed IPT_12months', m['MOH_Indicator_Name']) != None and 'TB_PREV' in d['DATIM_Indicator_Category']:
                if re.search("([<]|[+]", dk0) != None and re.search('(Female|Male|Unknown Sex)', dk0) != None and re.search('(Newly Enrolled|Previously Enrolled)', dk0) != None and m['facility'] == d['facility']:
                    #print("{}\t<= Completed IPT_12months =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                    found = True
                    append_data(temp_dict, m, d, 0)
                    datimydict.remove(datimydict[j])
                    break
            else:
                if (d['DATIM_Indicator_Category'] == 'TX_CURR') and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 M|F
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None and re.match(m['facility'], d['facility']) != None:
                        #print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None and re.match(m['facility'], d['facility']) != None:
                        #print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    #15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(m['facility'], d['facility']) != None:
                        #print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(m['facility'],j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'HTS_TST') and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 Positive M|F
                    if get_regex_value("((Positive)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", dk0) != None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(m['facility'], d['facility']) != None:
                        #print("{}\t<= positive to positive mapping ageles =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Positive Unknown Sex
                    elif get_regex_value("((Positive)\s+[<](\d+)\s+(\w+)\s+(\w+))") != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None and re.match(m['facility'], d['facility']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Positive M|F
                    elif get_regex_value("((Positive)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(m['facility'], d['facility']) != None:
                        #print("{}\t<= positive to positive mapping ageplus =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative M|F Positive
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(ageset, mk0) != None and (mageset < dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        #print("{}\t<= negative to pstve|tested ageless sub =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative M|F Tested
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.search(ageset, mk0) != None and (mageset < dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        #print("{}\t<= negative to pstve|tested ageless add  =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative|Positive  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(ageset, mk0) != None and (mageset < dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative|Tested  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.search(ageset, mk0) != None and (mageset < dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        #print("{}\t<= negative to pstve|tested mapping ageless sex unknown =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Negative M|F Positive
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Negative M|F Tested
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Tested", mk0).group() != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'PMTCT_ART') and re.search("Total", dk0) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                    if re.search("On HAART at 1st ANC", m['MOH_Indicator_Name']) != None and m['facility'] == d['facility']:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif re.search("Start HAART_ANC", m['MOH_Indicator_Name']) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'PMTCT_STAT') and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                    if get_regex_value("((Known)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Known Positive at 1st  ANC", m['MOH_Indicator_Name']) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif get_regex_value("((Newly)\s+(\w+)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Positive Results_ANC", m['MOH_Indicator_Name']) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif re.search("((New)\s+(\w+)\s+(\w+))", dk0) != None and re.match("Initial test at ANC", m['MOH_Indicator_Name']) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif re.search("((New)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Positive Results_ANC", m['MOH_Indicator_Name']) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'TX_NEW') and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 M|F
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        #print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset < dageset and re.search(ageset, mk0) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        #print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    #15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and mageset >= dageset and re.search(ageset, mk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(m['facility'], d['facility']) != None and re.match(m['ward'], d['ward']) != None:
                        #print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(m['facility'],j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
        # if found:
        #  continue
    # print(temp_dict)
    temp_df = pd.DataFrame(temp_dict)
    temp_df.drop_duplicates(inplace=True)
    return temp_df


@api_view()
def generate_comparison_file(request, use_api_data, category, county, from_date, to_date):
    try:
        datim_df = get_datim_non_null_values(category, county)
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
            print(moh_df.info())
            mohdict = moh_df.to_dict(orient='records')
        print(datim_df.head(1))
        print(moh_df.head(1))
        if len(mohdict) <= 0:
            return Response({"message": "Could not find data to process!"})
        temp_df = compare_data(mohdict, datimdict)
        temp_df['weight'] = temp_df.datim_data/temp_df.datim_data.sum()
        # calculate concodance
        temp_df['concodance(%)'] = (temp_df['weight']*100*(((temp_df['khis_data']+temp_df['datim_data']) -
                                                            abs(temp_df['khis_data']-temp_df['datim_data']))/(temp_df['khis_data']+temp_df['datim_data'])))
        temp_df['khis_minus_datim'] = temp_df['khis_data'] - \
            temp_df['datim_data']
        final_dict = temp_df.to_dict(orient='records')
        for record in final_dict:
            final_data, created = final_comparison_data.objects.get_or_create(
                facility=record['facility'],
                ward=record['ward'],
                subcounty=record['subcounty'],
                county=record['county'],
                MOH_FacilityID=record['MOH_FacilityID'],
                DATIM_Disag_ID=record['DATIM_Disag_ID'],
                MOH_IndicatorCode=record['MOH_IndicatorCode'],
                indicators=record['indicators'],
                DATIM_Disag_Name=record['DATIM_Disag_Name'],
                khis_data=record['khis_data'],
                datim_data=record['datim_data'],
                weight=record['weight'],
                concodance=record['concodance(%)'],
                khis_minus_datim=record['khis_minus_datim'])
        print(temp_df['concodance(%)'].sum())
        print(final_data)
        return Response({"message": "Data Comparison mapping for {} completed successfully!".format(str(county))})
    except Exception as e:
        print("mapping error:{}".format(e))
        return Response({"error": str(e)})


class GetMappedFiles(generics.ListAPIView):
    serializer_class = mappedDataSerializer
    permission_classes = ()

    def get_queryset(self):
        return mapped_data.objects.all()

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


def ABSOLUTE_PATH():
    return Path(__file__).resolve().parent.parent


def load_mapping_csv(category, qouter):
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


def load_datim_csv(category, county, fromdate):
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping_files")
    # print(MEDIA_ROOT)
    folder_path = MEDIA_ROOT
    res = []
    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    print(res)
    try:
        datimfile = os.path.join(
            folder_path,  [i for i in res if re.search(str(category).lower(), str(i).lower()) != None][0])
    except Exception as e:
        datimfile = ''
        print(e)
    if datimfile != '':
        year = int(datetime.now().year)
        cols = ["orgunitlevel2", "orgunitlevel2", "orgunitlevel3", "orgunitlevel4", "orgunitlevel5", "organisationunitid",
                "dataid", "dataname", "Oct to Dec {}".format(year-1), "Jan to Mar {}".format(year), "Apr to Jun {}".format(year)]
        datim_df = pd.read_csv(datimfile, usecols=cols)
        print(datim_df)
        datim_df.insert(0, 'DATIM_Indicator_Category', str(
            (str(category).upper()+',')*datim_df.shape[0]).split(",")[:-1], True)
        # add created date filter fo tx_curr
        year = int(datetime.now().year)
        if str(fromdate) == '{}-10-01'.format(year-1):
            datim_df.drop(columns=["Jan to Mar {}".format(
                year), "Apr to Jun {}".format(year)], inplace=True)
            datim_df.rename(columns={"Oct to Dec {}".format(
                year-1): "datim_data"}, inplace=True)
            datim_df['created'] = '{}-10-01'.format(year-1)
        elif str(fromdate) == '{}-01-01'.format(year):
            datim_df.drop(columns=["Oct to Dec {}".format(
                year-1), "Apr to Jun {}".format(year)], inplace=True)
            datim_df.rename(columns={"Jan to Mar {}".format(
                year): "datim_data"}, inplace=True)
            datim_df['created'] = '{}-01-01'.format(year)
        elif str(fromdate) == '{}-04-01'.format(year):
            datim_df.drop(columns=["Oct to Dec {}".format(
                year-1), "Jan to Mar {}".format(year)], inplace=True)
            datim_df.rename(columns={"Apr to Jun {}".format(
                year-1): "datim_data"}, inplace=True)
            datim_df['created'] = '{}-04-01'.format(year)
        elif str(fromdate) == '{}-07-01'.format(year):
            datim_df.drop(columns=["Oct to Dec {}".format(
                year-1), "Jan to Mar {}".format(year)], inplace=True)
            datim_df.rename(columns={"Jul to Sept {}".format(
                year-1): "datim_data"}, inplace=True)
            datim_df['created'] = '{}-07-01'.format(year)
        else:
            datim_df.rename(columns={"Oct to Dec {}".format(
                year-1): "datim_data"}, inplace=True)
            datim_df['created'] = '{}-10-01'.format(year-1)
        # UID Mappings
        # datim_cats = pd.merge(load_mapping_csv(category, county), datim_df,
        #                       on='DATIM_Disag_ID', how='inner')
        # datim_df = datim_cats
        datim_df.rename(columns={'organisationunitid': 'DATIM_UID', 'orgunitlevel2': 'county',
                        'orgunitlevel3': 'subcounty', 'orgunitlevel4': 'ward', 'orgunitlevel5': 'facility', 'dataid': 'DATIM_Disag_ID', 'dataname': 'DATIM_Disag_Name'}, inplace=True)
        datim_df['DATIM_Indicator_Category'] = str(category).upper()

        if str(county).lower() != 'all' and str(category) != 'all':
            datim_df = datim_df.query(
                'DATIM_Indicator_Category == "{}" and county == "{}"'.format(category, county))
        else:
            pass
        datim_df.drop_duplicates(inplace=True)
    else:
        return pd.DataFrame([])
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
    cols = ["MOH_FacilityID", "facility", "ward", "subcounty",
            "county", "MOH_IndicatorCode", "inndicator", "Value", "Period"]
    moh_df = pd.read_csv(mohfile, usecols=cols)
    moh_df.rename(columns={'MOH_FacilityID': 'MOH_UID', 'Value': 'khis_data',
                  'inndicator': 'MOH_Indicator_Name', 'MOH_IndicatorCode': 'MOH_Indicator_ID'}, inplace=True)
    if str(county).lower() != 'all':
        moh_df = moh_df.query('county == "{}"'.format(county))
    else:
        pass
    moh_df.drop_duplicates(inplace=True)
    return moh_df


def get_datim_non_null_values(category, county, fromdate):
    try:
        datim_df = load_datim_csv(category, county, fromdate)
    except Exception as e:
        datim_df = pd.DataFrame()
        print(e)
    if not datim_df.empty:
        datim_df = datim_df[~datim_df['DATIM_Disag_ID'].isnull()]
        datim_df['datim_data'].fillna(0, inplace=True)  # Fill NaN values
        datim_df['datim_data'] = datim_df['datim_data'].astype(int)
        datim_df.drop_duplicates(inplace=True)
        datim_df = datim_df[datim_df.datim_data != 0]
        print(datim_df.head(1))
    else:
        return pd.DataFrame([])
    return datim_df.iloc[:1000]


def get_moh_non_null_values(county):
    moh_df = load_moh_csv(county)
    moh_df = moh_df[~moh_df['MOH_Indicator_ID'].isnull()]
    moh_df['khis_data'].fillna(0, inplace=True)  # Fill NaN values
    moh_df['khis_data'] = moh_df['khis_data'].astype(int)
    moh_df.drop_duplicates(inplace=True)
    moh_df = moh_df[moh_df.khis_data != 0]
    # year = int(datetime.now().year)
    moh_df['Period'] = moh_df['Period'].map(str)
    moh_df.insert(0, 'created', str(
        (',')*moh_df.shape[0]).split(",")[:-1], True)
    for i, dt in moh_df.Period.items():
        moh_df['created'][i] = "{}-{}-01".format(dt[:-2], dt[-2:])
    print(moh_df.head(1))
    return moh_df.iloc[:2000]


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
            'created': m['created'],
            'facility': m['facility'],
            'ward': m['ward'],
            'subcounty': m['subcounty'],
            'county': m['county'],
            'MOH_FacilityID': m['MOH_UID'],
            'MOH_IndicatorCode': m['MOH_Indicator_ID'],
            'category': d['DATIM_Indicator_Category'],
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
                    # print("{}\t<= Completed IPT_12months =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                    found = True
                    append_data(temp_dict, m, d)
                    datimdict.remove(datimdict[j])
                    break
            else:
                if (d['DATIM_Indicator_Category'] == 'TX_CURR'):
                    # <15 M|F
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
                        # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
                        # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # 15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        # print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(m['facility'],j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'HTS_TST'):
                    # <15 Positive M|F
                    if get_regex_value("((Positive)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", dk0) != None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        # print("{}\t<= positive to positive mapping ageles =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Positive Unknown Sex
                    elif get_regex_value("((Positive)\s+[<](\d+)\s+(\w+)\s+(\w+))") != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # 15+ Positive M|F
                    elif get_regex_value("((Positive)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        # print("{}\t<= positive to positive mapping ageplus =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Negative M|F Positive
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        # print("{}\t<= negative to pstve|tested ageless sub =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Negative M|F Tested
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        # print("{}\t<= negative to pstve|tested ageless add  =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Negative|Positive  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 Negative|Tested  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None:
                        # print("{}\t<= negative to pstve|tested mapping ageless sex unknown =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # 15+ Negative M|F Positive
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # 15+ Negative M|F Tested
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Tested", mk0).group() != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
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
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
                        # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None:
                        # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d)
                        datimdict.remove(datimdict[j])
                        break
                    # 15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None:
                        # print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(m['facility'],j,d['DATIM_Disag_Name'],i,m['MOH_Indicator_Name']))
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
    datimageset = ''
    mageset = 0
    datim_25_plus = 0
    found = False
    temp_dict = []
    # print(mohdict[0])
    # try:
    for i, m in enumerate(mohdict):
        for j, d in enumerate(datimydict):
            dk0 = d['DATIM_Disag_Name'].replace('|', '').replace(
                '|', '').split(':')[1].replace(',', '')
            mk0 = m['MOH_Indicator_Name'].replace('_', ' ').replace('(', ' (')
            # print(mk0)
            # print(dk0)
            # DATIM ageset
            # "(\d+)"
            datimagesetpattern = r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})"
            datimageset = get_regex_value(datimagesetpattern, dk0)
            if datimageset != None or '':
                check_datim_ageset = ""
                if re.search("[-]", datimageset) != None:
                    dageset = int(datimageset.split('-')[1])
                elif re.search("[+]", datimageset) != None:
                    dageset = int(datimageset.strip("+"))
                else:
                    dageset = int(datimageset.strip('<'))
                # map to <15
                if dageset == 1:
                    dk0 = dk0.replace(datimageset, "<15")
                    check_datim_ageset = "<1"
                elif dageset > 1 and dageset <= 9:
                    dk0 = dk0.replace(datimageset, "<15")
                    check_datim_ageset = "1-9"
                elif dageset > 9 and dageset <= 14:  # <15
                    dk0 = dk0.replace(datimageset, "<15")
                    check_datim_ageset = "10-14"
                # map to 15+
                if dageset > 15 and dageset <= 19:  # 15+
                    dk0 = dk0.replace(datimageset, "15+")
                    check_datim_ageset = "15-19"
                elif dageset > 19 and dageset <= 24:  # 15+
                    dk0 = dk0.replace(datimageset, "15+")
                    check_datim_ageset = "20-24"
                if dageset >= 25:  # 15+ 50-54
                    dk0 = dk0.replace(datimageset, "15+")
                    datim_25_plus = 25
            # print(dk0)
            # MOH ageset
            pattern = r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})"
            moh_ageset = get_regex_value(pattern, mk0)
            ageset = get_regex_value(pattern, mk0)
            if ageset != None or '':
                if re.search("[-]", ageset):
                    mageset = int(ageset.split('-')[1])
                elif re.search("[+]", ageset) != None:
                    mageset = int(ageset.strip("+"))
                else:
                    mageset = int(ageset.strip('<'))
            # print("mageset:{} - dageset:{} <=> ageset:{}".format(mageset, dageset, ageset))
            # print(ageset)
            # check gender
            if re.search("[r'('][F][r')']", mk0) != None:
                gender = 'Female'
            elif re.search("[r'('][M][r')']", mk0) != None:
                gender = 'Male'
            else:
                gender = 'Unknown Sex'
            # print(gender)
            mfacility = str(m['facility']).split(' ')[0]
            dfacility = str(d['facility']).split(' ')[0]
            if re.search('Completed IPT_12months', m['MOH_Indicator_Name']) != None or re.search('Completed IPT_6months', m['MOH_Indicator_Name']) != None and re.search('TB_PREV', d['DATIM_Indicator_Category']) != None:
                # re.search("([<]|[+]", dk0) != None and re.search('(Female|Male|Unknown Sex)', dk0) != None and re.search('(Newly Enrolled|Previously Enrolled)', dk0) != None and
                if re.match(mfacility, dfacility) != None:
                    print("{}\t<= Completed IPT_12months =>\t{}".format(
                        d['DATIM_Disag_Name'], m['MOH_Indicator_Name']))
                    found = True
                    append_data(temp_dict, m, d, 0)
                    datimydict.remove(datimydict[j])
                    break
            else:
                if (d['DATIM_Indicator_Category'] == 'TX_CURR') and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 M|F 10-14 <1 1-9
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and dageset <= mageset and re.match(ageset, check_datim_ageset) != None and re.match(mfacility, dfacility) != None:
                        print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and dageset <= mageset and re.match(ageset, check_datim_ageset) != None and re.match(mfacility, dfacility) != None:
                        print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and mageset != datim_25_plus and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None:
                        # import pdb
                        print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            m['facility'], j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        # pdb.set_trace()
                        break
                    # 25+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and mageset == datim_25_plus and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None:
                        print("datim:{} <=>\tmoh:{}".format(d, m))
                        import pdb
                        found = True
                        temp_dict_check_df = pd.DataFrame(temp_dict)
                        if not temp_dict_check_df.query('"{}" in DATIM_Disag_Name and "{}" in DATIM_Disag_Name'.format([re.match(datimagesetpattern, i['DATIM_Disag_Name']).group() for i in temp_dict if int(re.match(datimagesetpattern, i['DATIM_Disag_Name']).group().split('-')[1] >= 25)][0], gender)).empty:
                            temp_dict = [(i['datim_data']+d['datim_data']) for i in temp_dict if int(
                                re.match(datimagesetpattern, i['DATIM_Disag_Name']).group().split('-')[1] >= 25)]
                        else:
                            append_data(temp_dict, m, d, 0)
                            datimydict.remove(datimydict[j])
                        pdb.set_trace()
                        break
                elif (d['DATIM_Indicator_Category'] == 'TX_NEW') and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 M|F 10-14 <1 1-9
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.search(gender, dk0) != None and dageset <= mageset and re.match(ageset, check_datim_ageset) != None and re.match(mfacility, dfacility) != None:
                        print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and dageset <= mageset and re.match(ageset, check_datim_ageset) != None and re.match(mfacility, dfacility) != None:
                        print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and mageset != datim_25_plus and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None:
                        print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            m['facility'], j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 25+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and mageset == datim_25_plus and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None:
                        print("datim:{} <=>\tmoh:{}".format(d, m))
                        found = True
                        temp_dict_check_df = pd.DataFrame(temp_dict)
                        if temp_dict_check_df.query('DATIM_Disag_ID == "{}"'.format(d['DATIM_Disag_ID'])) != None:
                            for item in temp_dict:
                                if item['DATIM_Disag_ID'] == d['DATIM_Disag_ID'] and item['DATIM_Disag_Name'] == d['DATIM_Disag_Name']:
                                    temp_dict['datim_data'] = temp_dict['datim_data'] + \
                                        d['datim_data']
                                    break
                        else:
                            append_data(temp_dict, m, d, 0)
                            datimydict.remove(datimydict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'HTS_TST') and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 Positive M|F
                    if get_regex_value("((Positive)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", dk0) != None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None:
                        print("{}\t<= positive to positive mapping ageles =>\t{}".format(
                            d['DATIM_Disag_Name'], m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Positive Unknown Sex
                    elif get_regex_value("((Positive)\s+[<](\d+)\s+(\w+)\s+(\w+))") != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, check_datim_ageset) != None and re.match(mfacility, dfacility) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Positive M|F
                    elif get_regex_value("((Positive)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None:
                        # print("{}\t<= positive to positive mapping ageplus =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative M|F Positive
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        # print("{}\t<= negative to pstve|tested ageless sub =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative M|F Tested
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        # print("{}\t<= negative to pstve|tested ageless add  =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative|Positive  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative|Tested  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.match(ageset, check_datim_ageset) != None and (mageset <= dageset) and re.search("[r'(']["+gender[:1]+"][r')']", mk0) == None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        # print("{}\t<= negative to pstve|tested mapping ageless sex unknown =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Negative M|F Positive
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Negative M|F Tested
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Tested", mk0).group() != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, check_datim_ageset) != None and re.search("[r'(']["+gender[:1]+"][r')']", mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'PMTCT_ART') and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                    dk0 = "Start HAART_ANC"
                    if get_regex_value(dk0, mk0) != None and re.match(mfacility, dfacility):
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif re.search("On HAART at 1st ANC", m['MOH_Indicator_Name']) != None and re.match(mfacility, dfacility):
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif re.search("Start HAART_ANC", m['MOH_Indicator_Name']) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'PMTCT_STAT') and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                    # New ANC clients 15+ M|F
                    if get_regex_value("(\w+)\s+(\w+)\s+(\w+)\s+(\d+)[+]\s+(\w+)", dk0) and get_regex_value("Initial test at ANC", mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # New ANC clients <15 M|F
                    elif get_regex_value("(\w+)\s+(\w+)\s+(\w+)\s+[<](\d+)\s+(\w+)", dk0) and get_regex_value("Initial test at ANC", mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif get_regex_value("((Known)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Known Positive at 1st  ANC", m['MOH_Indicator_Name']) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif get_regex_value("((Newly)\s+(\w+)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Positive Results_ANC", m['MOH_Indicator_Name']) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif re.search("((New)\s+(\w+)\s+(\w+))", dk0) != None and re.match("Initial test at ANC", m['MOH_Indicator_Name']) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    elif re.search("((New)\s+(\w+)\s+(\w+))", dk0) != None and re.search("Positive Results_ANC", m['MOH_Indicator_Name']) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
        if found:
            continue
    # print(temp_dict)
    temp_df = pd.DataFrame(temp_dict)
    temp_df.drop_duplicates(inplace=True)
    return temp_df


@ api_view()
def generate_comparison_file(request, use_api_data, category, county, from_date, to_date):
    # try:
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

import pandas as pd
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
import datetime
from django.utils import timezone
from django.db.models import Q


def ABSOLUTE_PATH():
    return Path(__file__).resolve().parent.parent


def load_datim_csv():
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping")
    # print(MEDIA_ROOT)
    folder_path = MEDIA_ROOT
    res = []
    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    print(res)
    datimfile = os.path.join(folder_path, res[-1])
    # print(datimfile)
    datim_df = pd.read_csv(datimfile)
    return datim_df


def load_moh_csv():
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\final")

    # print(MEDIA_ROOT)
    folder_path1 = MEDIA_ROOT
    res1 = []
    for path1 in os.listdir(folder_path1):
        if os.path.isfile(os.path.join(folder_path1, path1)):
            res1.append(path1)
    # print(res1)
    mohfile = os.path.join(folder_path1, res1[-1])
    moh_df = pd.read_csv(mohfile)
    return moh_df


def get_NaN_Values():
    datim_df = load_datim_csv()
    NaN_Values_df = datim_df[datim_df['Operation'].isnull()]
    return NaN_Values_df


def get_non_null_values():
    datim_df = load_datim_csv()
    datim_df = datim_df[~datim_df['Operation'].isnull()]
    return datim_df


@api_view()
def map_data(request):
    datim_df = get_non_null_values()
    datimydict = datim_df.to_dict(orient='records')
    moh_df = load_moh_csv()
    mohdict = []
    moh_csv_dict = moh_df.to_dict(orient='records')
    # add moh 731 to db
    # for j in moh_csv_dict:
    #     mohdata, created = indicators.objects.get_or_create(MOH_Indicator_Name=str(j['MOH_Indicator_Name']), MOH_Indicator_ID=str(
    #         j['MOH_Indicator_ID']), created=timezone.now(), lastUpdated=timezone.now())
    # print(mohdata)
    for i in indicators.objects.filter(Q(MOH_Indicator_Name__icontains='MOH 731')):
        mohdict.append({'MOH_Indicator_Name': str(i.MOH_Indicator_Name),
                       'MOH_Indicator_ID': str(i.MOH_Indicator_ID), 'MOH_Disag_Name': '', 'MOH_Disag_ID': '', 'Disaggregation Type': 'Coarse'})
    print(mohdict)
    temp_dict = []
    gender = ''
    dageset = ''
    mageset = ''
    try:
        for i, d in enumerate(datimydict):
            for j, m in enumerate(mohdict):
                dk0 = d['DATIM_Disag_Name'].replace('|', '').split()
                mk0 = m['MOH_Indicator_Name'].replace(
                    '_', ' ').replace('(', ' (').split()
                print(mk0)
                print(dk0)
                # check ageset
                # DATIM ageset
                ageresless = [a for a in dk0 if "<" in a]
                ageresplus = [a1 for a1 in dk0 if "+" in a1]
                if ageresplus:
                    ageresplus = int(ageresplus[0].replace('+', ''))
                    dageset = ageresplus
                if ageresless:
                    ageresless = int(ageresless[0].replace('<', ''))
                    dageset = ageresless
                # print(ageset)
                # MOH ageset
                mageles = [idx for idx in mk0 if any(chr.isdigit() for chr in idx) and not any(
                    chr.isalpha() for chr in idx) and any('-' in chr for chr in idx[:3])]
                if mageles:
                    # print(mageles)
                    mageset = int(mageles[0].split('-')[1])
                    print("=->"+str(mageset))
                else:
                    mageplus = [idx for idx in mk0 if "+" in idx[:3]]
                    if mageplus:
                        mageset = int(mageplus[0].replace('+', ''))
                        # print(mageplus)
                        print("=+>"+str(mageset))
                # print(mageset)
                # check gender
                if "F" in str(mk0):
                    gender = 'Female'
                elif "M" in str(mk0):
                    gender = 'Male'
                else:
                    gender = 'Unknown Sex'

                if (d['DATIM_Indicator_Category'] == 'HTS_TST') and ('Positive' in str(mk0)) and ('Positive' in str(dk0)):
                    if ('<' in str(dk0)) and ("1-9" in str(mk0) or "10-14" in str(mk0)) and (mageset < dageset) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        # print("{}\t<= positive to positive mapping ageles =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ('Positive | <15 | Unknown Sex' in d['DATIM_Disag_Name']) and (mageset < dageset) and ("(M)" not in str(mk0) and "(F)" not in str(mk0)):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ('+' in str(dk0)) and ("15-19" in str(mk0) or "20-24" in str(mk0) or "25+" in str(mk0)) and (mageset > dageset) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        # print("{}\t<= positive to positive mapping ageplus =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                elif (d['DATIM_Indicator_Category'] == 'HTS_TST') and ('Negative' in str(dk0)) and ('Positive' in str(mk0) or 'Tested' in str(mk0)):
                    if ('<' in str(dk0)) and ('Positive' in str(mk0)) and (d['Operation'] == 'SUBTRACT') and ("1-9" in str(mk0) or "10-14" in str(mk0)) and (mageset < dageset) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        # print("{}\t<= negative to pstve|tested ageless sub =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ('<' in str(dk0)) and ('Tested' in str(mk0)) and (d['Operation'] == 'ADD') and ("1-9" in str(mk0) or "10-14" in str(mk0)) and (mageset < dageset) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        # print("{}\t<= negative to pstve|tested ageless add  =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ('Negative | <15 | Unknown Sex' in d['DATIM_Disag_Name']) and (d['Operation'] == 'SUBTRACT') and (mageset < dageset) and ("(M)" not in str(mk0) and "(F)" not in str(mk0)) and ("Positive" in str(mk0)):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ('Negative | <15 | Unknown Sex' in d['DATIM_Disag_Name']) and (d['Operation'] == 'ADD') and (mageset < dageset) and ("(M)" not in str(mk0) and "(F)" not in str(mk0)) and ("Tested" in str(mk0)):
                        # print("{}\t<= negative to pstve|tested mapping ageless sex unknown =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ('+' in str(dk0)) and ('Positive' in str(mk0)) and (d['Operation'] == 'SUBTRACT') and ("15-19" in str(mk0) or "20-24" in str(mk0) or "25+" in str(mk0)) and (mageset > dageset) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        # print("{}\t<= negative to pstve|tested ageplus sub =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ('+' in str(dk0)) and ('Tested' in str(mk0)) and (d['Operation'] == 'ADD') and ("15-19" in str(mk0) or "20-24" in str(mk0) or "25+" in str(mk0)) and (mageset > dageset) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        # print("{}\t<= negative to pstve|tested ageplus add =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                elif (d['DATIM_Indicator_Category'] == 'PMTCT_ART') and ("Total" in str(dk0)):
                    if ("On HAART at 1st ANC" in m['MOH_Indicator_Name']):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("Start HAART_ANC" in m['MOH_Indicator_Name']):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                elif (d['DATIM_Indicator_Category'] == 'PMTCT_STAT'):
                    if ("Known Positive | Female" in d['DATIM_Disag_Name']) and ("Known Positive at 1st  ANC       HV02-03" in m['MOH_Indicator_Name']):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("Newly Tested Positive | Female" in d['DATIM_Disag_Name']) and ("Positive Results_ANC       HV02-11" in m['MOH_Indicator_Name']):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("New Negative | Female" in d['DATIM_Disag_Name']) and (d['Operation'] == 'ADD') and ("Initial test at ANC       HV02-04" in m['MOH_Indicator_Name']):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("New Negative | Female" in d['DATIM_Disag_Name']) and (d['Operation'] == 'SUBTRACT') and ("Positive Results_ANC       HV02-11" in m['MOH_Indicator_Name']):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                elif (d['DATIM_Indicator_Category'] == 'TX_CURR'):
                    if ("<" in str(dk0)) and (mageset < dageset) and ("On ART" in m['MOH_Indicator_Name']) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("<15 | Unknown Sex" in d['DATIM_Disag_Name']) and (mageset < dageset) and (" On ART" in m['MOH_Indicator_Name']) and ("1-9" in str(mk0) or "10-14" in str(mk0)) and ("<1" not in str(mk0)) and ("(M)" not in str(mk0) and "(F)" not in str(mk0)):
                        # print("{}\t<= TX_NEW =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("<15 | Unknown Sex" in d['DATIM_Disag_Name']) and (" On ART" in m['MOH_Indicator_Name']) and ("<1" in str(mk0) or "10-14" in str(mk0)) and ("(M)" not in str(mk0) and "(F)" not in str(mk0)):
                        # print("{}\t<= TX_NEW =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("+" in str(dk0)) and (mageset > dageset) and ("On ART" in m['MOH_Indicator_Name']) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                elif (d['DATIM_Indicator_Category'] == 'TX_NEW'):
                    if ("<" in str(dk0)) and (mageset < dageset) and ("Start ART" in m['MOH_Indicator_Name']) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("+" in str(dk0)) and (mageset > dageset) and ("Start ART" in m['MOH_Indicator_Name']) and (gender in str(dk0)) and ("("+gender[:1]+")" in str(mk0)):
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("<15 | Unknown Sex" in d['DATIM_Disag_Name']) and (mageset < dageset) and ("Start ART" in m['MOH_Indicator_Name']) and ("1-9" in str(mk0) or "10-14" in str(mk0)) and ("<1" not in str(mk0)) and ("(M)" not in str(mk0) and "(F)" not in str(mk0)):
                        # print("{}\t<= TX_NEW =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
                    elif ("<15 | Unknown Sex" in d['DATIM_Disag_Name']) and ("Start ART" in m['MOH_Indicator_Name']) and ("<1" in str(mk0) or "10-14" in str(mk0)) and ("(M)" not in str(mk0) and "(F)" not in str(mk0)):
                        # print("{}\t<= TX_NEW =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        temp_dict.append({
                            'DATIM_Indicator_Category': d['DATIM_Indicator_Category'],
                            'DATIM_Indicator_ID': d['DATIM_Indicator_ID'],
                            'DATIM_Disag_Name': d['DATIM_Disag_Name'],
                            'DATIM_Disag_ID': d['DATIM_Disag_ID'],
                            'Operation': d['Operation'],
                            'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
                            'MOH_Indicator_ID': m['MOH_Indicator_ID'],
                            'MOH_Disag_Name': m['MOH_Disag_Name'],
                            'MOH_Disag_ID': m['MOH_Disag_ID'],
                            'Disaggregation Type': m['Disaggregation Type']
                        })
        # print(temp_dict)
        temp_df = pd.DataFrame(temp_dict)
        temp_df.drop_duplicates(inplace=True)
        # print(temp_df)
        temp_df.info()
        NaN_df = get_NaN_Values()
        final_df = temp_df.append(NaN_df, ignore_index=True)
        final_df.tail(2)
        final_df.info()
        final_dict = final_df.to_dict(orient='records')
        # print(final_dict)
        for j in final_dict:
            final_data, created = mapped_data.objects.get_or_create(DATIM_Indicator_Category=str(
                j['DATIM_Indicator_Category']), DATIM_Indicator_ID=str(j['DATIM_Indicator_ID']), DATIM_Disag_ID=str(j['DATIM_Disag_ID']), DATIM_Disag_Name=str(j['DATIM_Disag_Name']), Operation=str(j['Operation']), MOH_Indicator_Name=str(j['MOH_Indicator_Name']), MOH_Indicator_ID=str(j['MOH_Indicator_ID']), MOH_Disag_Name=str(j['MOH_Disag_Name']), MOH_Disag_ID=str(j['MOH_Disag_ID']), Disaggregation_Type=str(j['Disaggregation Type']))
            print(final_data)
        final_df.to_csv(os.path.join(os.path.join(ABSOLUTE_PATH(), 'media\\mapped'),
                        'Final_Datim_Mapped_Csv_File.csv'), index=False)
        return Response({"Success": "Data Mapping completed successfully!"})
    except Exception as e:
        print(e)
        return Response({"Error": str(e)})


class GetMappedFiles(generics.ListAPIView):
    serializer_class = mappedDataSerializer
    permission_classes = ()

    def get_queryset(self):
        return mapped_data.objects.all()

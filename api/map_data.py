import re
from datetime import timedelta
from datetime import datetime
from pathlib import Path
import json
from .serializers import *
from .models import *
import os
import pandas as pd
# from mapping_rules.models import *
from .dataset_regex import *


def append_data(mydict, m, d, check=1):
    mydict.append({
        'created': m['created'],
        'facility': m['facility'],
        'ward': m['ward'],
        'subcounty': m['subcounty'],
        'county': m['county'],
        'MOH_FacilityID': m['MOH_UID'],
        'MOH_IndicatorCode': m['MOH_Indicator_ID'],
        'DATIM_Disag_ID': d['DATIM_Disag_ID'],
        'category': d['DATIM_Indicator_Category'],
        'MOH_Indicator_Name':  m['MOH_Indicator_Name'],
        'DATIM_Disag_Name': d['DATIM_Disag_Name'],
        'khis_data': m['khis_data'],
        'datim_data': d['datim_data'],
    })


def extract_age_group(element):
    age_group = re.search(
        r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})", element).group()
    # print(element, age_group)
    try:
        if 'MOH' not in element:
            if end_limit(age_group) >= 15:
                age_group = "15+"
                element = str(element).replace(age_group, "15+")
            elif (end_limit(age_group) >= 10) and (end_limit(age_group) <= 14):
                age_group = "10-14"
                element = str(element).replace(age_group, "10-14")
            elif (end_limit(age_group) >= 2) and (end_limit(age_group) <= 9):
                element = str(element).replace(age_group, "1-9")
                age_group = "1-9"
        return age_group
    except Exception as e:
        print("age:{}".format(e))

# Define a function to extract gender from khis elements


def extract_gender(element):
    try:
        age_group = re.search(
            r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})", element).group()
        if age_group in ["<1", "1-9", "1-4", "5-9"]:
            gender = "Unknown Sex"
            return gender
        else:
            # check gender
            gender = re.search(r"\((F|M)\)|(Male|Female)", element).group()
            if gender == '(F)':
                gender = "Female"
            elif gender == '(M)':
                gender = "Male"
            # print(gender)
        return gender
    except Exception as e:
        print("gender:{}".format(e))

# Define a function to find the most similar datim element for a khis element


def similarity(khis_name, datim_name):
    try:
        max_similarity = 0
        max_similarity = max_similarity + sum([1 for word in str(khis_name).replace("_", " ").replace(
            "(F)", " Female").replace("(M)", " Male").split()
            if word.lower() in str(datim_name).replace(",", "").lower()])
        return max_similarity
    except Exception as e:
        print(e)
    return max_similarity


def end_limit(age_group):
    try:
        end_limit = int(re.findall(r'\d+', age_group)[-1])
        return end_limit
    except Exception as e:
        print(e)


def rename_datim(element):
    age_group = re.search(
        r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})", element).group()
    try:
        if ('TX_NEW' or 'TX_CURR') in element:
            if end_limit(age_group) >= 15:
                element = str(element).replace(age_group, "15+")
            elif (end_limit(age_group) >= 10) and (end_limit(age_group) <= 14):
                element = str(element).replace(age_group, "10-14")
            elif (end_limit(age_group) >= 2) and (end_limit(age_group) <= 9):
                element = str(element).replace(age_group, "1-9")
        return element
    except Exception as e:
        print("age:{}".format(e))


def map_data(mohdict, datimydict):
    # Map khis elements to datim elements
    mapped_list = []
    for i, d in enumerate(datimydict):
        try:
            next = False
            exists = False
            d['DATIM_Disag_Name'] = rename_datim(d['DATIM_Disag_Name'])
            datim_name = d['DATIM_Disag_Name']
            datim_age = extract_age_group(datim_name)
            datim_gender = extract_gender(datim_name)
            for j, m in enumerate(mohdict):
                if next:
                    break
                khis_name = m['MOH_Indicator_Name']
                khis_age = extract_age_group(khis_name)
                khis_gender = extract_gender(khis_name)
                # print(max_limit(datim_age))
                # print(max_limit(khis_age))
                # <1 Unknown gender
                if (end_limit(datim_age) <= 1 and end_limit(khis_age)<=1) and (datim_age in khis_age) and (datim_gender in khis_gender):
                    data_range = 0
                    for element in mapped_list:
                        if datim_name in element['DATIM_Disag_Name']:
                            data_range = int(
                                element['khis_data'])-int(element['datim_data'])
                            if (data_range <= 1) or (data_range == 0):
                                exists = False
                            else:
                                element['datim_data'] += int(
                                    d['datim_data'])
                                mohdict.remove(mohdict[j])
                                exists = True
                                data_range = int(
                                    element['khis_data'])-int(element['datim_data'])
                                if (data_range <= 1) or (data_range == 0):
                                    next = True
                                break
                    if not exists:
                        append_data(mapped_list, m, d)
                        mohdict.remove(mohdict[j])
                        next = True
                        break
                 # <15 M|F 1-9
                elif ((end_limit(datim_age) >= 1 and end_limit(datim_age)<=9) and (end_limit(khis_age) >= 1 and end_limit(khis_age)<=9)) and (datim_age in khis_age) and (datim_gender in khis_gender):
                    data_range = 0
                    for element in mapped_list:
                        if datim_name in element['DATIM_Disag_Name']:
                            data_range = int(
                                element['khis_data'])-int(element['datim_data'])
                            if (data_range <= 1) or (data_range == 0):
                                exists = False
                            else:
                                element['datim_data'] += int(
                                    d['datim_data'])
                                mohdict.remove(mohdict[j])
                                exists = True
                                data_range = int(
                                    element['khis_data'])-int(element['datim_data'])
                                if (data_range <= 1) or (data_range == 0):
                                    next = True
                                break
                    if not exists:
                        append_data(mapped_list, m, d)
                        mohdict.remove(mohdict[j])
                        next = True
                        break
                # <15 M|F 10-14
                elif ((end_limit(datim_age) >= 10 and end_limit(datim_age)<=14) and (end_limit(khis_age) >= 10 and end_limit(khis_age)<=14)) and (datim_age in khis_age) and (datim_gender in khis_gender):
                    data_range = 0
                    for element in mapped_list:
                        if datim_name in element['DATIM_Disag_Name']:
                            data_range = int(
                                element['khis_data'])-int(element['datim_data'])
                            if (data_range <= 1) or (data_range == 0):
                                exists = False
                            else:
                                element['datim_data'] += int(
                                    d['datim_data'])
                                mohdict.remove(mohdict[j])
                                exists = True
                                data_range = int(
                                    element['khis_data'])-int(element['datim_data'])
                                if (data_range <= 1) or (data_range == 0):
                                    next = True
                                break
                    if not exists:
                        append_data(mapped_list, m, d)
                        mohdict.remove(mohdict[j])
                        next = True
                        break
                # 15+ M|F 15-19
                elif ((end_limit(datim_age) >= 15 and end_limit(datim_age) <=19) and (end_limit(khis_age) >= 15 and end_limit(khis_age)<=19)) and (datim_age in khis_age) and (datim_gender in khis_gender):
                    data_range = 0
                    for element in mapped_list:
                        if datim_name in element['DATIM_Disag_Name']:
                            data_range = int(
                                element['khis_data'])-int(element['datim_data'])
                            if (data_range <= 1) or (data_range == 0):
                                exists = False
                            else:
                                element['datim_data'] += int(
                                    d['datim_data'])
                                mohdict.remove(mohdict[j])
                                exists = True
                                data_range = int(
                                    element['khis_data'])-int(element['datim_data'])
                                if (data_range <= 1) or (data_range == 0):
                                    next = True
                                break
                    if not exists:
                        append_data(mapped_list, m, d)
                        mohdict.remove(mohdict[j])
                        next = True
                        break
                # 15+ M|F 20-24
                elif ((end_limit(datim_age) >= 20 and end_limit(datim_age)<=24) and (end_limit(khis_age) <= 20 and end_limit(khis_age)<=24)) and (datim_age in khis_age) and (datim_gender in khis_gender):
                    data_range = 0
                    for element in mapped_list:
                        if datim_name in element['DATIM_Disag_Name']:
                            data_range = int(
                                element['khis_data'])-int(element['datim_data'])
                            if (data_range <= 1) or (data_range == 0):
                                exists = False
                            else:
                                element['datim_data'] += int(
                                    d['datim_data'])
                                mohdict.remove(mohdict[j])
                                exists = True
                                data_range = int(
                                    element['khis_data'])-int(element['datim_data'])
                                if (data_range <= 1) or (data_range == 0):
                                    next = True
                                break
                    if not exists:
                        append_data(mapped_list, m, d)
                        mohdict.remove(mohdict[j])
                        next = True
                        break
                    # 15+ M|F 25+
                elif ((end_limit(datim_age) >= 25) and (end_limit(khis_age) >= 25)) and (datim_age in khis_age) and (datim_gender in khis_gender):
                    data_range = 0
                    for element in mapped_list:
                        if datim_name in element['DATIM_Disag_Name']:
                            data_range = int(
                                element['khis_data'])-int(element['datim_data'])
                            if (data_range <= 1) or (data_range == 0):
                                exists = False
                            else:
                                element['datim_data'] += int(
                                    d['datim_data'])
                                mohdict.remove(mohdict[j])
                                exists = True
                                data_range = int(
                                    element['khis_data'])-int(element['datim_data'])
                                if (data_range <= 1) or (data_range == 0):
                                    next = True
                                break
                    if not exists:
                        append_data(mapped_list, m, d)
                        mohdict.remove(mohdict[j])
                        next = True
                        break
        except Exception as e:
            print("mapping:{}".format(e))
    temp_df = pd.DataFrame(mapped_list)
    temp_df.drop_duplicates(inplace=True)
    return temp_df

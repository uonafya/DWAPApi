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
        if age_group.endswith("+"):
            age_group = "25+"
            element = str(element).replace(age_group, "25+")
        elif "-" in age_group and int(age_group.split("-")[1]) >= 25:
            age_group = "25+"
            element = str(element).replace(age_group, "25+")
            element = str(element).replace(age_group, "25+")
        elif "-" in age_group and (int(age_group.split("-")[1]) >= 1 and int(age_group.split("-")[1]) <= 9):
            element = str(element).replace(age_group, "1-9")
            age_group = "1-9"
        # print(age_group)
        # print(element)
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


def find_similar_datim(khis_name, datim_element):
    try:
        max_similarity = 3
        most_similar_datim = {}
        similarity = sum([1 for word in str(str(khis_name).split()).replace("_", " ").replace(
            "(F)", " Female").replace("(M)", " Male")
            if word.lower() in str(datim_element['DATIM_Disag_Name']).replace(",", "").lower()])
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_datim = datim_element
            # print("Most similar=>", khis_name, most_similar_datim)
        else:
            most_similar_datim = None
    except Exception as e:
        print(e)
    return most_similar_datim


def group_datim_elem(element):
    age_group = re.search(
        r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})", element).group()
    try:
        if age_group.endswith("+"):
            element = str(element).replace(age_group, "25+")
        elif '-' in age_group and int(age_group.split("-")[1]) >= 25:
            element = str(element).replace(age_group, "25+")
        elif "-" in age_group and (int(age_group.split("-")[1]) >= 1 and int(age_group.split("-")[1]) <= 9):
            element = str(element).replace(age_group, "1-9")
        elif "<" in age_group and int(age_group.split("<")[1]) <= 1:
            element = str(element).replace(age_group, "<1")
        # print(element)
        return element
    except Exception as e:
        print("age:{}".format(e))


def merge_grouped_elememts(dict_list, d, datim_name):
    try:
        match_found = False
        for element in dict_list:
            if element[datim_name] == datim_name and (extract_age_group(datim_name) == '25+' or extract_age_group(datim_name) == '1-9'):
                element['datim_data'] += int(d['datim_data'])
                match_found = True
        print(match_found, element, datim_name)
        return match_found
    except Exception as e:
        print("merge elem:{}".format(e))


def map_data(mohdict, datimydict):
    # Map khis elements to datim elements
    mapped_list = []
    group_datim_elements = True
    for i, d in enumerate(datimydict):
        try:
            next = False
            exists = False
            # m['name'] = group_elem(m['name'])
            if group_datim_elements:
                d['DATIM_Disag_Name'] = group_datim_elem(d['DATIM_Disag_Name'])
            datim_name = d['DATIM_Disag_Name']
            datim_age = extract_age_group(datim_name)
            datim_gender = extract_gender(datim_name)
            for j, m in enumerate(mohdict):
                if next:
                    break
                khis_name = m['MOH_Indicator_Name']
                khis_age = extract_age_group(khis_name)
                khis_gender = extract_gender(khis_name)
                # print(datim_gender, khis_gender)
                if datim_age in khis_age and datim_gender in khis_gender and find_similar_datim(khis_name, d) != None:
                    data_range = 0
                    # group and merge all age groups above or below 9
                    if [i for i in ['25+', '1-9'] if i in datim_name]:
                        for element in mapped_list:
                            if datim_name in element['DATIM_Disag_Name']:
                                data_range = int(
                                    element['khis_data'])-int(element['datim_data'])
                                if (data_range <= 5) or (data_range == 0):
                                    exists = False
                                else:
                                    element['datim_data'] += int(
                                        d['datim_data'])
                                    mohdict.remove(mohdict[j])
                                    exists = True
                                    data_range = int(
                                        element['khis_data'])-int(element['datim_data'])
                                    if (data_range <= 5) or (data_range == 0):
                                        next = True
                                    break
                        if not exists:
                            append_data(mapped_list, m, d)
                            mohdict.remove(mohdict[j])
                            next = True
                            break
                    else:
                        data_range = int(
                            element['khis_data'])-int(element['datim_data'])
                        if (data_range <= 5) or (data_range == 0):
                            next = True
                            append_data(mapped_list, m, d)
                            mohdict.remove(mohdict[j])
                            break
                        next = False
        except Exception as e:
            print("mapping:{}".format(e))
    temp_df = pd.DataFrame(mapped_list)
    temp_df.drop_duplicates(inplace=True)
    return temp_df

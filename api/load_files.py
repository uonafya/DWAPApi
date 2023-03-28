import re
from django.utils import timezone
from datetime import datetime
from pathlib import Path
import json
from .serializers import *
from .models import *
from mapping_rules.models import *
import os
import pandas as pd


def ABSOLUTE_PATH():
    return Path(__file__).resolve().parent.parent


def load_mapping_csv(category, qouter=""):
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping_files")
    # print(MEDIA_ROOT)
    folder_path = MEDIA_ROOT
    res = []
    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    # print(res)
    mapping = os.path.join(
        folder_path,  [i for i in res if re.search('indicatorMapping', i) != None][0])
    # print(datimfile)
    mapping_df = pd.read_csv(
        mapping, usecols=['DATIM_Indicator_Category', 'DATIM_Indicator_ID', 'DATIM_Disag_ID'])
    if str(category).lower() != "all":
        mapping_df = mapping_df.query(
            'DATIM_Indicator_Category == "{}"'.format(category))
    mapping_df.drop_duplicates(inplace=True)
    # print(mapping_df)
    return mapping_df


def load_datim_csv(category, county, fromdate):
    date_str = str(fromdate)
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    print(date_obj)

    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping_files")
    datast_grouping = GruopSeriesData.objects.get(dataset_name='datim')
    # print(MEDIA_ROOT)
    folder_path = MEDIA_ROOT
    res = []
    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            res.append(path)
    # print(res)
    try:
        if str(category) != 'all':
            datimfile = os.path.join(
                folder_path,  [i for i in res if re.search(str(category).lower(), str(i).lower()) != None][0])
        else:
            datimfile = os.path.join(
                folder_path,  [i for i in res if re.search(str(category).lower, str(i).lower()) != None][0])
    except Exception as e:
        datimfile = ''
        print(e)
    # import pdb
    if datimfile != '':
        year = date_obj.year
        print(year)
        cols = ["orgunitlevel2", "orgunitlevel2", "orgunitlevel3", "orgunitlevel4", "orgunitlevel5", "organisationunitid",
                "dataid", "dataname", "Oct to Dec {}".format(year-1), "Jan to Mar {}".format(year), "Apr to Jun {}".format(year)]
        datim_df = pd.read_csv(datimfile, usecols=cols)
        # print(datim_df)
        datim_df.insert(0, datast_grouping.group_by, str(
            (str(category).upper()+',')*datim_df.shape[0]).split(",")[:-1], True)
        # add created date filter fo tx_curr
        year = int(datetime.now().year)-1
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
            datim_df.drop(columns=["Apr to Jun {}".format(
                year), "Jan to Mar {}".format(year)], inplace=True)
            datim_df.rename(columns={"Oct to Dec {}".format(
                year-1): "datim_data"}, inplace=True)
            datim_df['created'] = '{}-10-01'.format(year-1)
        # UID Mappings
        # datim_cats = pd.merge(load_mapping_csv(category, county), datim_df,
        #                       on='DATIM_Disag_ID', how='inner')
        # datim_df = datim_cats
        datim_df.rename(columns={'organisationunitid': 'DATIM_UID', 'orgunitlevel2': 'county',
                        'orgunitlevel3': 'subcounty', 'orgunitlevel4': 'ward', 'orgunitlevel5': 'facility', 'dataid': 'DATIM_Disag_ID', 'dataname': 'DATIM_Disag_Name'}, inplace=True)
        #datim_df['DATIM_Indicator_Category'] = str(category).upper()

        # print(datim_df)

        if str(county).lower() != 'all':
            # print(county)
            datim_df = datim_df.query(f"county == '{county}'")
            # print(datim_df)
        datim_df.drop_duplicates(inplace=True)
        # pdb.set_trace()
        # print(datim_df)
        return datim_df
    else:
        return pd.DataFrame([])


def rename_columns(original_cols, new_cols):
    return {k: v for k, v in zip(original_cols, new_cols)}


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
        # print(datim_df.head(1))
        # print(datim_df)
        return datim_df.sample(n=2000, replace=True)  # datim_df.iloc[:2000]
    else:
        return pd.DataFrame([])


def load_moh_csv(county):
    print(county)
    MEDIA_ROOT = os.path.join(ABSOLUTE_PATH(), "media\\mapping_files")

    # print(MEDIA_ROOT)
    # import pdb
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
        moh_df = moh_df.query(f'county == "{county}"')
        #print(moh_df, county)
    moh_df.drop_duplicates(inplace=True)
    # pdb.set_trace()
    return moh_df


def get_moh_non_null_values(county):
    # import pdb
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
    moh_df.drop(columns=["Period"], inplace=True)
    # print(moh_df)
    # pdb.set_trace()
    return moh_df.sample(n=2000)  # moh_df.iloc[:2000]


# def get_datim_NaN_Values():
#     datim_df = load_datim_csv()
#     NaN_Values_df = datim_df[datim_df['DATIM_Disag_ID'].isnull()]
#     return NaN_Values_df


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

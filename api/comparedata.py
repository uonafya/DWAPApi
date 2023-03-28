import re
from datetime import timedelta
from datetime import datetime
from pathlib import Path
import json
from .serializers import *
from .models import *
import os
import pandas as pd
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


def get_regex_value(pattern, s):
    try:
        x = re.search(pattern, s).group()
        return x
    except Exception as e:
        print(e)


def map_data(mohdict, datimydict):
    gender = ''
    dageset = 0
    ageset = ''
    datimageset = ''
    mageset = 0
    datim_25_plus = False
    found = False
    temp_dict = []
    # print(mohdict[0])
    # try:
    for i, m in enumerate(mohdict):
        for j, d in enumerate(datimydict):
            dk0 = d['DATIM_Disag_Name'].replace('|', '').replace(
                '|', '').split(':')[1].replace(',', '')
            mk0 = m['MOH_Indicator_Name'].replace(
                '_', ' ').replace('(', ' (')
            # print(mk0)
            # print(dk0)
            # DATIM ageset
            # "(\d+)"
            datimageset = get_regex_value(ageset_pattern, dk0)
            if datimageset != None or '':
                mapt_to_khis_ageset = ""
                if re.search("[-]", datimageset) != None:
                    dageset = int(datimageset.split('-')[1])
                elif re.search("[+]", datimageset) != None:
                    dageset = int(datimageset.strip("+"))
                else:
                    dageset = int(datimageset.strip('<'))
                # map to <15
                if dageset == 1:
                    dk0 = dk0.replace(datimageset, "<15")
                    mapt_to_khis_ageset = "<1"
                elif dageset > 1 and dageset <= 9:
                    dk0 = dk0.replace(datimageset, "<15")
                    mapt_to_khis_ageset = "1-9"
                elif dageset > 9 and dageset <= 14:  # <15
                    dk0 = dk0.replace(datimageset, "<15")
                    mapt_to_khis_ageset = "10-14"
                # map to 15+
                if dageset > 15 and dageset <= 19:  # 15+
                    dk0 = dk0.replace(datimageset, "15+")
                    mapt_to_khis_ageset = "15-19"
                elif dageset > 19 and dageset <= 24:  # 15+
                    dk0 = dk0.replace(datimageset, "15+")
                    mapt_to_khis_ageset = "20-24"
                elif dageset >= 25:  # 15+ 50-54
                    dk0 = dk0.replace(datimageset, "15+")
                    datim_25_plus = True
            # print(dk0)
            # MOH ageset
            #moh_ageset_pattern = r"(\d{2}[+])|(\d+[-]\d+)|([<]\d{1})"
            moh_ageset = get_regex_value(ageset_pattern, mk0)
            #ageset = get_regex_value(ageset_pattern, mk0)
            if moh_ageset != None or '':
                if re.search("[-]", moh_ageset):
                    mageset = int(moh_ageset.split('-')[1])
                elif re.search("[+]", moh_ageset) != None:
                    mageset = int(moh_ageset.strip("+"))
                else:
                    mageset = int(moh_ageset.strip('<'))
            # print("mageset:{} - dageset:{} <=> ageset:{}".format(mageset, dageset, ageset))
            # print(ageset)
            # check gender
            if re.search(female_gender_regex, mk0) != None:
                gender = 'Female'
            elif re.search(male_gender_regex, mk0) != None:
                gender = 'Male'
            else:
                gender = 'Unknown Sex'

            moh_gender = "[r'(']["+gender[:1]+"][r')']"
            # print(gender)
            mfacility = str(m['facility']).split(' ')[0]
            dfacility = str(d['facility']).split(' ')[0]
            if re.search('TB_PREV', d['DATIM_Indicator_Category']) != None and (re.search('Completed IPT_12months', m['MOH_Indicator_Name']) != None or re.search('Completed IPT_6months', m['MOH_Indicator_Name']) != None):
                # re.search("([<]|[+]", dk0) != None and re.search('(Female|Male|Unknown Sex)', dk0) != None and re.search('(Newly Enrolled|Previously Enrolled)', dk0) != None and
                if re.match(mfacility, dfacility) != None:
                    # print("{}\t<= Completed IPT_12months =>\t{}".format(
                    #     d['DATIM_Disag_Name'], m['MOH_Indicator_Name']))
                    found = True
                    append_data(temp_dict, m, d, 0)
                    datimydict.remove(datimydict[j])
                    break
            else:
                if (d['DATIM_Indicator_Category'] == 'TX_CURR') and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 M|F 10-14 <1 1-9
                    if get_regex_value(less_15_regex_m_f, dk0) != None and re.search(moh_gender, mk0) != None and re.search(gender, dk0) != None and dageset <= mageset and re.match(ageset, mapt_to_khis_ageset) != None and re.match(mfacility, dfacility) != None:
                        # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                        #     j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value(less_15_regex_unknown, dk0) != None and re.search(moh_gender, mk0) == None and re.search(gender, dk0) != None and dageset <= mageset and re.match(ageset, mapt_to_khis_ageset) != None and re.match(mfacility, dfacility) != None:
                        # print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                        #     j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ M|F
                    elif get_regex_value(plus_15_m_f, dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, mapt_to_khis_ageset) != None and datim_25_plus == False and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None:
                        # import pdb
                        # print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                        #     m['facility'], j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        # pdb.set_trace()
                        break
                    # 25+ M|F
                    elif get_regex_value(plus_25_m_f, dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and datim_25_plus == True and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None:
                        print("datim:{} <=>\tmoh:{}".format(d, m))
                        # import pdb
                        found = True
                        # temp_dict_check_df = pd.DataFrame(temp_dict)
                        # if not temp_dict_check_df.query('"{}" in DATIM_Disag_Name and "{}" in DATIM_Disag_Name'.format([re.match(datimagesetpattern, i['DATIM_Disag_Name']).group() for i in temp_dict if int(re.match(datimagesetpattern, i['DATIM_Disag_Name']).group().split('-')[1] >= 25)][0], gender)).empty:
                        #     temp_dict = [(i['datim_data']+d['datim_data']) for i in temp_dict if int(
                        #         re.match(datimagesetpattern, i['DATIM_Disag_Name']).group().split('-')[1] >= 25)]
                        # else:
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        # pdb.set_trace()
                        break
                elif (d['DATIM_Indicator_Category'] == 'TX_NEW') and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 M|F 10-14 <1 1-9
                    if get_regex_value("([<]\d+\s+(\w+))", dk0) != None and re.search(moh_gender, mk0) != None and re.search(gender, dk0) != None and dageset <= mageset and re.match(ageset, mapt_to_khis_ageset) != None and re.match(mfacility, dfacility) != None:
                        print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 1-9|<1 unknown sex
                    elif get_regex_value("([<]\d+\s+(\w+)\s+(\w+))", dk0) != None and re.search(moh_gender, mk0) == None and re.search(gender, dk0) != None and dageset <= mageset and re.match(ageset, mapt_to_khis_ageset) != None and re.match(mfacility, dfacility) != None:
                        print("{}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, mapt_to_khis_ageset) != None and datim_25_plus == False and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None:
                        print("Facility:{} - {}=>{}\t<= TX_CURR =>\t{}=>{}".format(
                            m['facility'], j, d['DATIM_Disag_Name'], i, m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 25+ M|F
                    elif get_regex_value("(\d+[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and datim_25_plus == True and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None:
                        print("datim:{} <=>\tmoh:{}".format(d, m))
                        found = True
                        # temp_dict_check_df = pd.DataFrame(temp_dict)
                        # if temp_dict_check_df.query('DATIM_Disag_ID == "{}"'.format(d['DATIM_Disag_ID'])) != None:
                        #     for item in temp_dict:
                        #         if item['DATIM_Disag_ID'] == d['DATIM_Disag_ID'] and item['DATIM_Disag_Name'] == d['DATIM_Disag_Name']:
                        #             temp_dict['datim_data'] = temp_dict['datim_data'] + \
                        #                 d['datim_data']
                        #             break
                        # else:
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                elif (d['DATIM_Indicator_Category'] == 'HTS_TST') and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                    # <15 Positive M|F
                    if get_regex_value("((Positive)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", dk0) != None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, mapt_to_khis_ageset) != None and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None:
                        print("{}\t<= positive to positive mapping ageles =>\t{}".format(
                            d['DATIM_Disag_Name'], m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Positive Unknown Sex
                    elif get_regex_value("((Positive)\s+[<](\d+)\s+(\w+)\s+(\w+))") != None and re.search(moh_gender, mk0) == None and re.search(gender, dk0) != None and mageset <= dageset and re.match(ageset, mapt_to_khis_ageset) != None and re.match(mfacility, dfacility) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Positive M|F
                    elif get_regex_value("((Positive)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, mapt_to_khis_ageset) != None and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None:
                        # print("{}\t<= positive to positive mapping ageplus =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative M|F Positive
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.match(ageset, mapt_to_khis_ageset) != None and (mageset <= dageset) and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        # print("{}\t<= negative to pstve|tested ageless sub =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative M|F Tested
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.match(ageset, mapt_to_khis_ageset) != None and (mageset <= dageset) and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        # print("{}\t<= negative to pstve|tested ageless add  =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative|Positive  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.match(ageset, mapt_to_khis_ageset) != None and (mageset <= dageset) and re.search(moh_gender, mk0) == None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # <15 Negative|Tested  Unknown Sex
                    elif get_regex_value("((Negative)\s+[<](\d+)\s+(\w+))", dk0) != None and re.search("Tested", mk0) != None and re.match(ageset, mapt_to_khis_ageset) != None and (mageset <= dageset) and re.search(moh_gender, mk0) == None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        # print("{}\t<= negative to pstve|tested mapping ageless sex unknown =>\t{}".format(d['DATIM_Disag_Name'],m['MOH_Indicator_Name']))
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Negative M|F Positive
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Positive", mk0) != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, mapt_to_khis_ageset) != None and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
                        found = True
                        append_data(temp_dict, m, d, 0)
                        datimydict.remove(datimydict[j])
                        break
                    # 15+ Negative M|F Tested
                    elif get_regex_value("((Negative)\s+(\d+)[+]\s+(\w+))", dk0) != None and re.search("Tested", mk0).group() != None and re.search(gender, dk0) != None and dageset >= mageset and re.match(ageset, mapt_to_khis_ageset) != None and re.search(moh_gender, mk0) != None and re.match(mfacility, dfacility) != None and re.match(m['ward'], d['ward']) != None:
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

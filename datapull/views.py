from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from .utils import PMTCTDataClient
from .models import *
from .serializers import *

import pandas as pd

class ScheduleView(APIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self, pk):
        try:
            return schedule_settings.objects.get(pk=pk)
        except schedule_settings.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        recs = schedule_settings.objects.all()
        serializer = ScheduleSerializer(
            recs, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MiddlewareSettingsViewSet(viewsets.ModelViewSet):
    queryset = middleware_settings.objects.all()
    serializer_class = middleware_settingSerializer
    permission_classes = ()

@api_view()
def sync_data(request):
    sets = middleware_settings.objects.all().first()
    return Response({"id": sets.id, "synctdata": str(sets.syncdata).lower(), "client_url": sets.client_url})

def classify(diff_anc):
    anc_status = ""
    if(diff_anc< 0):
        anc_status = "critical"
    elif(diff_anc>=0):
        anc_status = 'stable'
    else:
        anc_status='normal'
    return anc_status

def dataAnalytics(data):
    data_rows = pd.DataFrame(data['rows'])
    data_rows[3] = data_rows[3].astype(int)
    ana_lytics = {"data": []}
    try:
        if(len(data_rows)>0):
            org_units = data['metaData']['dimensions']['ou']
            print(org_units)
            for org in org_units:
                anc_status = ""
                moh_711_new_sum = 0
                moh_731_HV02_01_sum = 0
                org_data = {}
                moh_711_new = data_rows[(data_rows[0] == 'f9vesk5d4IY') & (data_rows[1] == org)]
                moh_731_HV02_01 = data_rows[(data_rows[0] == 'uSxBUWnagGg') & (data_rows[1] == org)]
                moh_731_HV02_03 = data_rows[(data_rows[0] == 'qSgLzXh46n9') & (data_rows[1] == org)]
                moh_731_HV02_04 = data_rows[(data_rows[0] == 'ETX9cUWF43c') & (data_rows[1] == org)]
                moh_731_HV02_05 = data_rows[(data_rows[0] == 'mQz4DhBSv9V') & (data_rows[1] == org)]
                moh_731_HV02_06 = data_rows[(data_rows[0] == 'LQpQQP3KnU1') & (data_rows[1] == org)]
                moh_731_HV02_10 = data_rows[(data_rows[0] == 'oZc8MNc0nLZ') & (data_rows[1] == org)]
                moh_731_HV02_11 = data_rows[(data_rows[0] == 'nwXS5vxrrr7') & (data_rows[1] == org)]
                moh_731_HV02_12 = data_rows[(data_rows[0] == 'hn3aChn4sVx') & (data_rows[1] == org)]
                moh_731_HV02_13 = data_rows[(data_rows[0] == 'AfHArvGun12') & (data_rows[1] == org)]
                moh_731_HV02_14 = data_rows[(data_rows[0] == 'hHLR1HP8xzI') & (data_rows[1] == org)]
                moh_731_HV02_16 = data_rows[(data_rows[0] == 'lJpaBye9B0H') & (data_rows[1] == org)]
                moh_731_HV02_17 = data_rows[(data_rows[0] == 'WNFWVHMqPv9') & (data_rows[1] == org)]
                moh_731_HV02_18 = data_rows[(data_rows[0] == 'ckPCoAwmWmT') & (data_rows[1] == org)]
                moh_731_HV02_19 = data_rows[(data_rows[0] == 'vkOYqEesPAi') & (data_rows[1] == org)]
                moh_731_HV02_21 = data_rows[(data_rows[0] == 'UMyB7dSIdz1') & (data_rows[1] == org)]
                moh_731_HV02_39 = data_rows[(data_rows[0] == 'HAumxpKBaoK') & (data_rows[1] == org)]
                moh_731_HV02_40 = data_rows[(data_rows[0] == 'Jn6ATTfXp02') & (data_rows[1] == org)]
                moh_731_HV02_41 = data_rows[(data_rows[0] == 'RY1js5pK2Ep') & (data_rows[1] == org)]

                org_name = data['metaData']['items'][org]['name']

                moh_711_new_sum = moh_731_HV02_01_sum = moh_731_HV02_03_sum = moh_731_HV02_04_sum = moh_731_HV02_05_sum = moh_731_HV02_06_sum = moh_731_HV02_10_sum = moh_731_HV02_11_sum = moh_731_HV02_12_sum = moh_731_HV02_13_sum = moh_731_HV02_14_sum = moh_731_HV02_16_sum = moh_731_HV02_17_sum = moh_731_HV02_18_sum = moh_731_HV02_19_sum = moh_731_HV02_21_sum = moh_731_HV02_39_sum = moh_731_HV02_40_sum = moh_731_HV02_41_sum = 0

                if(len(moh_711_new)> 0):
                    moh_711_new_sum = moh_711_new[3].sum()

                if(len(moh_731_HV02_01)> 0):
                    moh_731_HV02_01_sum = moh_731_HV02_01[3].sum()

                if(len(moh_731_HV02_03)> 0):
                    moh_731_HV02_03_sum = moh_731_HV02_03[3].sum()

                if(len(moh_731_HV02_04)> 0):
                    moh_731_HV02_04_sum = moh_731_HV02_04[3].sum()

                if(len(moh_731_HV02_05)> 0):
                    moh_731_HV02_05_sum = moh_731_HV02_05[3].sum()

                if(len(moh_731_HV02_06)> 0):
                    moh_731_HV02_06_sum = moh_731_HV02_06[3].sum()

                if(len(moh_731_HV02_10)> 0):
                    moh_731_HV02_10_sum = moh_731_HV02_10[3].sum()

                if(len(moh_731_HV02_11)> 0):
                    moh_731_HV02_11_sum = moh_731_HV02_11[3].sum()

                if(len(moh_731_HV02_12)> 0):
                    moh_731_HV02_12_sum = moh_731_HV02_12[3].sum()

                if(len(moh_731_HV02_13)> 0):
                    moh_731_HV02_13_sum = moh_731_HV02_13[3].sum()

                if(len(moh_731_HV02_14)> 0):
                    moh_731_HV02_14_sum = moh_731_HV02_14[3].sum()

                if(len(moh_731_HV02_16)> 0):
                    moh_731_HV02_16_sum = moh_731_HV02_16[3].sum()

                if(len(moh_731_HV02_17)> 0):
                    moh_731_HV02_17_sum = moh_731_HV02_17[3].sum()

                if(len(moh_731_HV02_18)> 0):
                    moh_731_HV02_18_sum = moh_731_HV02_18[3].sum()

                if(len(moh_731_HV02_19)> 0):
                    moh_731_HV02_19_sum = moh_731_HV02_19[3].sum()

                if(len(moh_731_HV02_21)> 0):
                    moh_731_HV02_21_sum = moh_731_HV02_21[3].sum()

                if(len(moh_731_HV02_39)> 0):
                    moh_731_HV02_39_sum = moh_731_HV02_39[3].sum()

                if(len(moh_731_HV02_40)> 0):
                    moh_731_HV02_40_sum = moh_731_HV02_40[3].sum()

                if(len(moh_731_HV02_41)> 0):
                    moh_731_HV02_41_sum = moh_731_HV02_41[3].sum()

                print(f"orgname: {org_name} moh_711_new_sum: {moh_711_new_sum}")
                diff_anc = moh_731_HV02_01_sum-moh_711_new_sum
                missed_opp = moh_731_HV02_01_sum - (moh_731_HV02_03_sum + moh_731_HV02_04_sum + moh_731_HV02_05_sum + moh_731_HV02_06_sum)


                anc_status = classify(diff_anc)
                # breakpoint()
                missed_opp_status = classify(diff_anc=-missed_opp)

                ana_lytics['data'].append({
                    "ou_name": org_name,
                    "moh_711_new": moh_711_new_sum,
                    "moh_731_HV02_01": moh_731_HV02_01_sum,
                    "diff_anc": diff_anc,
                    "anc_status": anc_status,
                    "moh_731_HV02_03": moh_731_HV02_03_sum,
                    "moh_731_HV02_04": moh_731_HV02_04_sum,
                    "moh_731_HV02_05": moh_731_HV02_05_sum,
                    "moh_731_HV02_06": moh_731_HV02_06_sum,
                    "moh_731_HV02_10": moh_731_HV02_10_sum,
                    "moh_731_HV02_11": moh_731_HV02_11_sum,
                    "moh_731_HV02_12": moh_731_HV02_12_sum,
                    "moh_731_HV02_13": moh_731_HV02_13_sum,
                    "moh_731_HV02_14": moh_731_HV02_14_sum,
                    "moh_731_HV02_16": moh_731_HV02_16_sum,
                    "moh_731_HV02_17": moh_731_HV02_17_sum,
                    "moh_731_HV02_18": moh_731_HV02_18_sum,
                    "moh_731_HV02_19": moh_731_HV02_19_sum,
                    "moh_731_HV02_21": moh_731_HV02_21_sum,
                    "moh_731_HV02_39": moh_731_HV02_39_sum,
                    "moh_731_HV02_40": moh_731_HV02_40_sum,
                    "moh_731_HV02_41": moh_731_HV02_41_sum,
                    "missed_opp": missed_opp,
                    "missed_opp_status": missed_opp_status,
                })
    except Exception as e:
        print(f" Error: {e}")
        ana_lytics['error'].append({"message": f"{e}"})
    return ana_lytics

class DataClientViewSet(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        ou:org_level & or g_id
        pe:period i.e 202309(sept 2023)
        """
        params = {
            'dimension': ['pe:202402','ou:LEVEL-5;fVra3Pwta0Q',
            'dx:f9vesk5d4IY;uSxBUWnagGg;qSgLzXh46n9;ETX9cUWF43c;mQz4DhBSv9V;LQpQQP3KnU1;oZc8MNc0nLZ;nwXS5vxrrr7;hn3aChn4sVx;AfHArvGun12;hHLR1HP8xzI;lJpaBye9B0H;WNFWVHMqPv9;ckPCoAwmWmT;vkOYqEesPAi;UMyB7dSIdz1;HAumxpKBaoK;Jn6ATTfXp02;RY1js5pK2Ep'],
            'outputIdScheme': 'UID'
        }
        credentials = ('testusercounty', '123456@Ab')
        url = f"https://hiskenya.org/api/analytics.json"
        client = PMTCTDataClient(url,params=params, credentials=credentials)
        data = client.pull_data()
        return Response(data)






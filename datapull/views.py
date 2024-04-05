from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from .utils import PMTCTDataClient

class DataClientViewSet(viewsets.ViewSet):
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        ou:org_level & org_id
        pe:period i.e 202309(sept 2023)
        """
        params = request.data.get('params',{
            'dimension': ['pe:202309', 'ou:LEVEL-5;fVra3Pwta0Q'],
            'outputIdScheme': 'NAME'
        })
        credentials = ('healthit', 'rr23H3@1th1Tmtct')
        url = "https://khis.pmtct.uonbi.ac.ke/api/29/analytics.json"
        client = PMTCTDataClient(url,params=params, credentials=credentials)
        data = client.pull_data()
        return Response(data)

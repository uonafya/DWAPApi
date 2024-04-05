import requests

class PMTCTDataClient:
    def __init__(self, url,params, credentials):
        self.params = params
        self.request_url = url
        self.credentials = credentials

    def pull_data(self):
        # Make the GET request with basic authentication
        response = requests.get(
            self.request_url, params=self.params, auth=self.credentials)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Process the response data (in JSON format)
            data = response.json()
            return data
        else:
            return {"Error": response.status_code}

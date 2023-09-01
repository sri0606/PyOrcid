import requests
from urllib.parse import urlencode


class Orcid():
    def __init__(self,client_id,client_secret,redirect_uri) -> None:
        self._redirect_uri = redirect_uri
        self._access_token = ""
        self._get_access_token(client_id,client_secret)
        return

    def _get_access_token(self,client_id,client_secret):
        '''
        Send a request to Postman API for Orcid's OAuth 2.0 authorrization
        '''
       # Set the necessary parameters
        redirect_uri = self._redirect_uri
        auth_url_endpoint = "https://orcid.org/oauth/authorize"
        token_url = "https://orcid.org/oauth/token"

        # Step 1: Redirect the user to the authorization URL
        params = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': '/authenticate'
        }
        auth_url = auth_url_endpoint + '?' + urlencode(params)
        print(f'Please go to this URL and authorize the app: {auth_url}')

        # Step 2: Get the authorization code from the redirect URL
        redirect_response = input('Paste the full redirect URL here: ')
        code = redirect_response.split('code=')[1].split('&')[0]

        # Step 3: Exchange the authorization code for an access token
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }

        response = requests.post(token_url, data=data)
        self._access_token = response.json().get('access_token')
        return None

    def read_orcid_record(self,orcid_id):
        '''
        '''
        # Set the headers with the access token for authentication
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json'
        }

        # # Specify the ORCID record endpoint for the desired ORCID iD
        api_url = f'https://pub.orcid.org/v3.0/{orcid_id}/record'

        # Make a GET request to retrieve the ORCID record
        response = requests.get(api_url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # The request was successful
            data = response.json()
            return data
        else:
            # Handle the case where the request failed
            print("Failed to retrieve ORCID data. Status code:", response.status_code)




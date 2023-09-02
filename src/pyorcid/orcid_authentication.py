import requests
from urllib.parse import urlencode
import os
from dotenv import load_dotenv,set_key


class OrcidAuthentication:
    def __init__(self, client_id, client_secret, redirect_uri):

        # Define the name of the .env file
        env_file = ".env"
        # Check if the .env file exists
        if not os.path.exists(env_file):
            # Create the .env file with default or initial values
            with open(env_file, "w") as file:
                # Set initial values
                file.write(f"ORCID_CLIENT_ID={client_id}\n")
                file.write(f"ORCID_CLIENT_SECRET={client_secret}\n")
                file.write(f"ORCID_REDIRECT_URI={redirect_uri}\n")
                file.write("ORCID_ACCESS_TOKEN=\n")

        self._get_access_token(client_id, client_secret, redirect_uri)
        return None
    

    def _get_access_token(self,client_id,client_secret,redirect_uri):
        '''
        Send a request to Postman API for Orcid's OAuth 2.0 authorrization
        '''

       # Set the necessary parameters
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
        access_token = response.json().get('access_token')
        set_key(".env", "ORCID_ACCESS_TOKEN", access_token)
        return None
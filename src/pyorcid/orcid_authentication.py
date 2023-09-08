import requests
from urllib.parse import urlencode
import os
from dotenv import set_key


class OrcidAuthentication:
    def __init__(self, client_id, client_secret, redirect_uri):

        # # Define the name of the .env file
        # env_file = ".env"
        # # Check if the .env file exists
        # if not os.path.exists(env_file):
        #     # Create the .env file with default or initial values
        #     with open(env_file, "w") as file:
        #         # Set initial values
        #         file.write(f"ORCID_CLIENT_ID={client_id}\n")
        #         file.write(f"ORCID_CLIENT_SECRET={client_secret}\n")
        #         file.write(f"ORCID_REDIRECT_URI={redirect_uri}\n")
        #         file.write("ORCID_ACCESS_TOKEN=\n")

        access_token = self._get_access_token(client_id, client_secret, redirect_uri)
        if access_token:
            print("This is the access token. Please retain this to access the ORCID record of the user that gave access along with their ORCID_ID.")
            print(access_token)
        return None
    

    def _get_access_token(self,client_id,client_secret,redirect_uri):
        '''
        Send a request to Postman API for Orcid's OAuth 2.0 authorrization
        '''

       # Set the necessary parameters
        auth_url_endpoint = "https://sandbox.orcid.org/oauth/authorize"
        token_url = "https://sandbox.orcid.org/oauth/token"

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
        # set_key(".env", "ORCID_ACCESS_TOKEN", access_token)
        return access_token
    
    def save_credentials(client_id, client_secret, redirect_uri, access_token):
        '''
        Save the credentials and access token to a file
        '''
        print("Do you want to save credentials along with the access token? (y/n)")
        choice = input().strip().lower()
        
        if choice == 'y':
            print("The details will be saved in 'orcid_credentials.env' in the current working directory.")
            print("Are you sure you want to continue? (y/n)")
            confirmation = input().strip().lower()
            
            if confirmation == 'y':
                # Save credentials and access token to a file
                with open('orcid_credentials.env', 'w') as file:
                    file.write(f'CLIENT_ID={client_id}\n')
                    file.write(f'CLIENT_SECRET={client_secret}\n')
                    file.write(f'REDIRECT_URI={redirect_uri}\n')
                    file.write(f'ACCESS_TOKEN={access_token}\n')
                print("Credentials and access token saved.")
            else:
                print("Credentials and access token not saved.")
        else:
            print("This is the access token. Please retain this to access the ORCID record of the user that gave access along with their ORCID_ID.")
            print(access_token)

        return None


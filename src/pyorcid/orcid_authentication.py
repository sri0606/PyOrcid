import requests
from urllib.parse import urlencode

class OrcidAuthentication:
    '''
    OrcidAuthentication is a class that handles the Orcid's OAuth 2.0 authorrization.
    The Orcid's OAuth 2.0 authorrization is used to access the ORCID record of the user that gave access.
    
    '''
    def __init__(self, client_id, client_secret, redirect_uri=""):
        '''
        initializes the ORCidAuthentication and gets the access token
        Parameters
        ----------
        client_id : str : client id obtained from the registered application
        client_secret : str : client secret obtained from the registered application
        redirect_uri : str : redirect uri obtained from the registered application

        returns :
        1) if redirect_uri id None/empty, returns access token for methods that doesn't need user authorization (eg., /read-public scope of public API)
        2) else, returns access token for methods that needs user authorization (eg., Member API or /read-limited scope of public API)
        '''
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri
        return None
    
    
    def get_private_access_token(self):
        '''
        Send a request for Orcid's OAuth 2.0 authorrization
        This method is used for Member API (read/update) and Public API's /read-limited scope
        Requires user authorization
        '''

       # Set the necessary parameters
        # auth_url_endpoint = "https://sandbox.orcid.org/oauth/authorize"   #for testing
        # token_url = "https://sandbox.orcid.org/oauth/token"               #for testing

        auth_url_endpoint = "https://orcid.org/oauth/authorize"
        token_url = "https://orcid.org/oauth/token"

        # Step 1: Redirect the user to the authorization URL
        params = {
            'client_id': self.__client_id,
            'response_type': 'code',
            'redirect_uri': self.__redirect_uri,
            'scope': '/authenticate'
        }
        auth_url = auth_url_endpoint + '?' + urlencode(params)
        print(f'Please go to this URL and authorize the app: {auth_url}')
        print("\n")
        # Step 2: Get the authorization code from the redirect URL
        redirect_response = input('Paste the full URL of the page you were redirected to after authorizing: ')
        code = redirect_response.split('code=')[1].split('&')[0]

        # Step 3: Exchange the authorization code for an access token
        data = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.__redirect_uri
        }

        response = requests.post(token_url, data=data)
        access_token = response.json().get('access_token')
        # set_key(".env", "ORCID_ACCESS_TOKEN", access_token)
        return access_token
    
    def get_public_access_token(self):
        """
        This method gets token for reading public data (/read-public scope) from Orcid.
        Doesnt' require user authentication 
        return: access token
        """
        scope='/read-public'
        token_url = "https://orcid.org/oauth/token"
        params = {
            'client_id': self.__client_id,
            'client_secret': self.__client_secret,
            'scope': scope,
            'grant_type': 'client_credentials'
        }
        headers = {'Accept': 'application/json'}

        try:
            response = requests.post(token_url, data=params, headers=headers)
            # # Raises an exception for HTTP errors
            response.raise_for_status() 

            access_token = response.json().get('access_token')
            return access_token

        except requests.exceptions.RequestException as e:
            print(f"Error during token retrieval: {e}")
            return None
        
    def save_credentials(self, access_token):
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
                    file.write(f'CLIENT_ID={self.__client_id}\n')
                    file.write(f'CLIENT_SECRET={self.__client_secret}\n')
                    file.write(f'REDIRECT_URI={self.__redirect_uri}\n')
                    file.write(f'ACCESS_TOKEN={access_token}\n')
                print("Credentials and access token saved.")
            else:
                print("Credentials and access token not saved.")
        else:
            print("This is the access token. Please retain this to access the ORCID record of the user that gave access along with their ORCID_ID.")
            print(access_token)

        return None


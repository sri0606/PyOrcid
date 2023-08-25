import requests
from requests_oauthlib import OAuth2Session

class Orcid():
    """
    
    """
    def __init__(self,client_id,client_secret,redirect_uri):
        # Replace with your actual values
        return self.__authorize(client_id,client_secret,redirect_uri)

    
    def __authorize(self,client_id,client_secret,redirect_uri):
        """
        
        """
        authorization_base_url = 'https://orcid.org/oauth/authorize'
        token_url = 'https://orcid.org/oauth/token'
        scopes = ['authenticate', 'openid', '/read-limited']

        # Step 1: Redirect user to the ORCID authorization page
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,scope=' '.join(scopes))
        authorization_url, state = oauth.authorization_url(authorization_base_url)

        print("Please go to the following URL and authorize the application:")
        print(authorization_url)

        # Step 2: Get authorization code from user and exchange it for an access token
        authorization_code = input("Enter the authorization code: ")
        token = oauth.fetch_token(token_url, code=authorization_code, client_secret=client_secret)

        # Use the obtained access token to make API requests
        access_token = token['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}

        # Example API request (replace with actual endpoint)
        api_url = 'https://pub.orcid.org/v3.0/0000-0002-1825-0097/record'
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Failed to retrieve data:", response.status_code)



my_orcid = Orcid(client_id="APP-G4D1E8X61HYNDAKJ",client_secret="0d9c5005-f3d2-4366-ab0c-ab92009e78e8",redirect_uri="https://github.com/sri0606/PyOrcid")

print(my_orcid)
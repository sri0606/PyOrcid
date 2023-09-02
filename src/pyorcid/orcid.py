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

    def read_record(self,orcid_id):
        '''
        Reads the Orcid record
        orcid_id: Orcid ID of the member
        return  : a dictionary of summary view of the full ORCID record 
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

    
    def person(self,orcid_id):
        '''
        Read biographical section of the ORCID record, including through /researcher-urls below
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    
    def address(self,orcid_id):
        '''
        The researcher's countries or regions
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def email(self,orcid_id):
        '''
        The email address(es) associated with the record
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def external_identifiers(self,orcid_id):
        '''
        Linked external identifiers in other systems
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def keywords(self,orcid_id):
        '''
        Keywords related to the researcher and their work
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def other_names(self,orcid_id):
        '''
        Other names by which the researcher is know
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def personal_details(self,orcid_id):
        '''
        Personal details: the researcher's name, credit (published) name, and biography
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def researcher_urls(self,orcid_id):
        '''
        Links to the researcher‚s personal or profile pages
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def activities(self,orcid_id):
        '''
        Summary of the activities section of the ORCID record, including through /works below.
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def educations(self,orcid_id):
        '''
        Education affiliations
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def employments(self,orcid_id):
        '''
        Employment affiliations
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def fundings(self,orcid_id):
        '''
        Summary of funding activities
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def peer_reviews(self,orcid_id):
        '''
        Summary of peer review activities
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def works(self,orcid_id):
        '''
        Summary of research works
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def research_resources (self,orcid_id):
        '''
        Summary of research resources 
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def services(self,orcid_id):
        '''
        Summary of services 
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def qualifications(self,orcid_id):
        '''
        Summary of qualifications 
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def memberships(self,orcid_id):
        '''
        Summary of memberships 
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def distinctions(self,orcid_id):
        '''
        Summary of distinctions 
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
    def invited_positions(self,orcid_id):
        '''
        Summary of invited positions
        orcid_id: Orcid ID of the member
        return  :
        '''
        return 
   


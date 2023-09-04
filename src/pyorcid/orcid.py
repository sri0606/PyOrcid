import requests
from dotenv import load_dotenv
import os

class Orcid():
    '''
    This is a wrapper class for ORCID API
    '''
    def __init__(self,orcid_id) -> None:
        '''
        Initialize orcid instance
        orcid_id : Orcid ID of the user
        '''
        self._orcid_id = orcid_id
        if not self.__is_access_token_valid():
             raise ValueError("Invalid access token! Please make sure you are authenticated by ORCID as developer.")

        return

    def __is_access_token_valid(self):
        '''
        Checks if the current access token is valid
        '''
        # Load environment variables from .env
        load_dotenv()

        # Access the environment variable
        access_token = os.getenv("ORCID_ACCESS_TOKEN")
        if access_token=="":
            raise ValueError("Empty value for access token! Please make sure you are authenticated by ORCID as developer.")
        # Make a test request to the API using the token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Replace with the appropriate test endpoint from the API
        test_api_url = f"https://pub.orcid.org/v3.0/{self._orcid_id}"

        response = requests.get(test_api_url, headers=headers)
        if response.status_code == 404:
            # The request was successful, and the token is likely valid
            return False
        else:
            # The request failed, indicating that the token may have expired or is invalid
            return True
        
    def __read_section(self,section="record"):
        '''
        Reads the section of a Orcid member Profile
        return  : a dictionary of summary view of the section of ORCID data 
        '''

        # Load environment variables from .env
        load_dotenv()

        # Access the environment variable
        access_token = os.getenv("ORCID_ACCESS_TOKEN")

        # Set the headers with the access token for authentication
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # # Specify the ORCID record endpoint for the desired ORCID iD
        api_url = f'https://pub.orcid.org/v3.0/{self._orcid_id}/{section}'

        # Make a GET request to retrieve the ORCID record
        response = requests.get(api_url, headers=headers)

        # The request was successful
        data = response.json()
        # Check the response status code
        if response.status_code == 200:
            return data
        else:
            # Handle the case where the request failed
            print("Failed to retrieve ORCID data. Status code:", response.status_code)
            return None

    def record(self):
        '''
        Reads the Orcid record
        return  : a dictionary of summary view of the full ORCID record 
        '''
        return self.__read_section("record")
    
    def person(self):
        '''
        Read biographical section of the ORCID record, including through /researcher-urls below
        return  :
        '''
        return self.__read_section("person") 
    
    def address(self):
        '''
        The researcher's countries or regions
        return  :
        '''
        return self.__read_section("address")  
    
    def email(self):
        '''
        The email address(es) associated with the record
        return  :
        '''
        return self.__read_section("email") 
    
    def external_identifiers(self):
        '''
        Linked external identifiers in other systems
        return  :
        '''
        return self.__read_section("external-identifiers") 
    
    def keywords(self):
        '''
        Keywords related to the researcher and their work
        return  :
        '''
        return self.__read_section("keywords") 
     
    def other_names(self):
        '''
        Other names by which the researcher is know
        return  :
        '''
        return self.__read_section("other-names") 
    
    def personal_details(self):
        '''
        Personal details: the researcher's name, credit (published) name, and biography
        return  :
        '''
        return self.__read_section("personal-details") 
    
    def researcher_urls(self):
        '''
        Links to the researcher‚s personal or profile pages
        return  :
        '''
        return self.__read_section("researcher-urls") 
    
    def activities(self):
        '''
        Summary of the activities section of the ORCID record, including through /works below.
        return  :
        '''
        return self.__read_section("activities") 
    
    def educations(self):
        '''
        Education affiliations
        return  :
        '''
        return self.__read_section("educations") 
    
    def employments(self):
        '''
        Employment affiliations
        return  :
        '''
        return self.__read_section("employments") 
    
    def fundings(self):
        '''
        Summary of funding activities
        return  :
        '''
        return self.__read_section("fundings") 
    
    def peer_reviews(self):
        '''
        Summary of peer review activities
        return  :
        '''
        return self.__read_section("peer-reviews") 
    
    def works(self):
        '''
        Summary of research works
        return  :
        '''
        return self.__read_section("works") 
    
    def research_resources (self):
        '''
        Summary of research resources 
        return  :
        '''
        return self.__read_section("research-resources") 
    
    def services(self):
        '''
        Summary of services 
        return  :
        '''
        return self.__read_section("services") 
    
    def qualifications(self):
        '''
        Summary of qualifications 
        return  :
        '''
        return self.__read_section("qualifications") 
    
    def memberships(self):
        '''
        Summary of memberships 
        return  :
        '''
        return self.__read_section("memberships") 
    
    def distinctions(self):
        '''
        Summary of distinctions 
        return  :
        '''
        return self.__read_section("distinctions") 
    
    def invited_positions(self):
        '''
        Summary of invited positions
        return  :
        '''
        return self.__read_section("invited-positions") 
    
    


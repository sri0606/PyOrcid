import requests
from dotenv import load_dotenv
import os

class Orcid():
    '''
    This is a wrapper class for ORCID API
    '''
    def __init__(self,orcid_id, orcid_access_token = " ", state="public") -> None:
        '''
        Initialize orcid instance
        orcid_id : Orcid ID of the user
        orcid_access_token : Orcid access token obtained from the user with this orcid_id
        state  : Whether to use public or member API of ORCID
        '''
        self._orcid_id = orcid_id
        self._access_token = orcid_access_token
        self._state = state
        #For testing purposes (pytesting on github workflow)
        try:
            self.__test_is_access_token_valid()
        except:
            if not self.__is_access_token_valid():
                raise ValueError(f"Invalid access token! Please make sure the user with ORCID_ID:{orcid_id} has given access.")

        return

    def __is_access_token_valid(self):
        '''
        Checks if the current access token is valid
        '''
        access_token = self.__access_token

        if access_token=="":
            raise ValueError("Empty value for access token! Please make sure you are authenticated by ORCID as developer.")
        # Make a test request to the API using the token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        api_url = ""

        if self._state == "public":
            # Specify the ORCID record endpoint for the desired ORCID iD
            api_url = f'https://pub.sandbox.orcid.org/v3.0/{self._orcid_id}'
            
        elif self._state == "member":
            api_url = f'https://api.sandbox.orcid.org/v3.0/{self._orcid_id}'

        response = requests.get(api_url, headers=headers)
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
        
        access_token = self.__access_token

        # Set the headers with the access token for authentication
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        api_url = ""

        if self._state == "public":
            # Specify the ORCID record endpoint for the desired ORCID iD
            api_url = f'https://pub.sandbox.orcid.org/v3.0/{self._orcid_id}/{section}'
            
        elif self._state == "member":
            api_url = f'https://api.sandbox.orcid.org/v3.0/{self._orcid_id}/{section}'

        # Make a GET request to retrieve the ORCID record
        response = requests.get(api_url, headers=headers)

        # The request was successful
        data = response.json()
        # Check the response status code
        if response.status_code == 200 or data is not None:
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
    
    def get_formatted_date(self,date_dict):
        """
        Formats a date dictionary into a string (e.g., "MM/YYYY") if all required keys are present and not None.

        Args:
            date_dict (dict): A dictionary containing 'year', 'month', and 'day' keys.

        Returns:
            str: The formatted date string or an empty string if any required key is missing or None.
        """
        if date_dict is not None:
            year = date_dict.get('year', {}).get('value') if date_dict.get('year', {}) else None
            month = date_dict.get('month', {}).get('value') if date_dict.get('month', {}) else None
            day = date_dict.get('day', {}).get('value') if date_dict.get('day', {}) else None

            # Check if all required keys are present and not None
            if year is not None and month is not None:
                return f"{month}/{year}"
            elif year is not None:
                return year
            else:
                return ''
        else:
            return ''


    def __extract_details(self,data, key):
        '''
        helper function for record_summary()
        '''
        details = []
        summary_key = key+'s'
        for summary in data['activities-summary'][summary_key]['affiliation-group']:
            for item in summary['summaries']:
                key_summary = item[f'{key}-summary']
                detail = {
                    'Department': key_summary.get('department-name', '') if 'department-name' in key_summary else '',
                    'Role': key_summary.get('role-title', '') if 'role-title' in key_summary else '',
                    'start-date': self.get_formatted_date(key_summary.get('start-date', {})),
                    'end-date': self.get_formatted_date(key_summary.get('end-date', {})),
                    'organization': key_summary.get('organization', {}).get('name', '') if 'organization' in key_summary else '',
                    'organization-address': ', '.join(filter(None, key_summary.get('organization', {}).get('address', {}).values())) if 'organization' in key_summary and 'address' in key_summary['organization'] else '',
                    'url': key_summary.get('url', {}).get('value', '') if 'url' in key_summary else '',
                    }
                details.append(detail)
        return details

    def record_summary(self):
        '''
        A cleaner version of Orcid record
        return  : a dictionary of summary view of the full ORCID record
        '''
        data = self.record()
        extracted_data = {
            'Name': data['person']['name']['given-names']['value'],
            'Biography': data['person']['biography']['content'],
            'Emails': [email['email'] for email in data['person']['emails']['email']],
            'Research Tags (keywords)': [keyword['content'] for keyword in data['person']['keywords']['keyword']],
        }

        # Extract education details
        education_details = self.__extract_details(data, 'education')
        if education_details: extracted_data['Education'] = education_details

        # Extract education details
        qualification_details = self.__extract_details(data, 'qualification')
        if qualification_details: extracted_data['Quaifications'] = qualification_details

        # Extract employment details
        employment_details = self.__extract_details(data, 'employment')
        if employment_details: extracted_data['Employment'] = employment_details

        # Extract education details
        distinction_details = self.__extract_details(data, 'distinction')
        if distinction_details: extracted_data['Distinctions'] = distinction_details

        # Extract employment details
        Invited_details = self.__extract_details(data, 'invited-position')
        if Invited_details: extracted_data['Invited Positions'] = Invited_details

        # Extract education details
        membership_details = self.__extract_details(data, 'membership')
        if membership_details: extracted_data['Memberships'] = membership_details

        # Extract service details
        service_details = self.__extract_details(data, 'service')
        if service_details: extracted_data['Service'] = service_details

        # Extract funding details with start and end dates
        funding_details = []
        for funding_summary in data['activities-summary']['fundings']['group']:
            for fund_summary in funding_summary['funding-summary']:
                funding_detail = {
                    'title': fund_summary['title']['title']['value'] if "title" in fund_summary and  "title" in fund_summary['title'] else '',
                    'type': fund_summary['type'] if "type" in fund_summary else '', 
                    'start-date': self.get_formatted_date(fund_summary.get('start-date', {})),
                    'end-date': self.get_formatted_date(fund_summary.get('end-date', {})),
                    'organization': fund_summary['organization']['name'] if "organization" in fund_summary and "name" in fund_summary['organization'] else '',
                    'organization-address': ', '.join(filter(None, fund_summary['organization']['address'].values())) if 'organization' in fund_summary and 'address' in fund_summary['organization'] else '',
                    'url': fund_summary['url']['value'] if 'url' in fund_summary else '',
                }
                funding_details.append(funding_detail)
        extracted_data['Fundings'] = funding_details

        work_details = []
        for working_summary in data['activities-summary']['works']['group']:
            for work_summary in working_summary['work-summary']:
                work_detail = {
                    'title': work_summary['title']['title']['value'] if "title" in work_summary and  "title" in work_summary['title'] else '',
                    'type': work_summary['type'] if "type" in work_summary else '', 
                    'publication-date': self.get_formatted_date(work_summary.get('publication-date', {})),
                    'journal title': work_summary['journal-title']['value'] if "journal-title" in work_summary else '',
                    'organization': work_summary['organization']['name'] if "organization" in work_summary and "name" in work_summary['organization'] else '',
                    'organization-address': ', '.join(filter(None, work_summary['organization']['address'].values())) if 'organization' in work_summary and 'address' in work_summary['organization'] else '',
                    'url': work_summary['url']['value'] if 'url' in work_summary else '',
                }
                work_details.append(work_detail)
        extracted_data['Works'] = work_details


        return extracted_data
    
    def generate_markdown_file(self, output_file=None):
        '''
        Generates a markdown file with the ORCID record summary
        output_file  : the name of the output file
        return  : None
        '''

        data = self.record_summary()
        if 'Name' in data:
            file_name = f"{data['Name']}.md"
        else:
            file_name = "output.md"  # Default file name if 'Name' field is missing

        if output_file is not None:
            file_name = output_file

        with open(file_name, 'w', encoding='utf-8') as md_file:
            for section, content in data.items():
                md_file.write(f"## {section}\n\n")
                
                if isinstance(content, list):
                    if content:
                        if isinstance(content[0], dict):
                            keys = content[0].keys()
                            md_file.write("| " + " | ".join(keys) + " |\n")
                            md_file.write("| " + " | ".join(["---"] * len(keys)) + " |\n")
                            for item in content:
                                md_file.write("| " + " | ".join(str(item[key]) for key in keys) + " |\n")
                        else:
                            for item in content:
                                md_file.write("- " + f"{item}\n")
                    else:
                        md_file.write("No data available.\n")
                else:
                    md_file.write(f"{content}\n")
                
                md_file.write("\n")



    ## THESE FUNCTIONS ARE FOR TESTING PURPOSES ##
    def __test_is_access_token_valid(self):
        '''
        FOR TESTING PURPOSES ONLY
        Checks if the current access token is valid
        '''
        # Access the environment variable from github secrets
        access_token = os.environ["ORCID_ACCESS_TOKEN"]
        if access_token=="":
            raise ValueError("Empty value for access token! Please make sure you are authenticated by ORCID as developer.")
        # Make a test request to the API using the token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        api_url = ""

        if self._state == "public":
            # Specify the ORCID record endpoint for the desired ORCID iD
            api_url = f'https://pub.sandbox.orcid.org/v3.0/{self._orcid_id}'
            
        elif self._state == "member":
            api_url = f'https://api.sandbox.orcid.org/v3.0/{self._orcid_id}'

        response = requests.get(api_url, headers=headers)
        if response.status_code == 404:
            # The request was successful, and the token is likely valid
            return False
        else:
            # The request failed, indicating that the token may have expired or is invalid
            return True
        
    def __test_read_section(self,section="record"):
        '''
        FOR TESTING PURPOSES ONLY
        Reads the section of a Orcid member Profile
        return  : a dictionary of summary view of the section of ORCID data 
        '''

        access_token = os.environ["ORCID_ACCESS_TOKEN"]

        # Set the headers with the access token for authentication
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        api_url = ""

        if self._state == "public":
            # Specify the ORCID record endpoint for the desired ORCID iD
            api_url = f'https://pub.sandbox.orcid.org/v3.0/{self._orcid_id}/{section}'
            
        elif self._state == "member":
            api_url = f'https://api.sandbox.orcid.org/v3.0/{self._orcid_id}/{section}'

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

    def __test_record(self):
        '''
        FOR TESTING PURPOSES ONLY
        Reads the Orcid record
        return  : a dictionary of summary view of the full ORCID record 
        '''
        return self.__test_read_section("record")
    

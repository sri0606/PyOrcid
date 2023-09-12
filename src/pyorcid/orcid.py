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
        self._orcid_access_token = orcid_access_token
        self._state = state
        #For testing purposes (pytesting on github workflow)
        if orcid_access_token!=" ":
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
        access_token = self._orcid_access_token

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
            # api_url = f'https://pub.sandbox.orcid.org/v3.0/{self._orcid_id}'  #for testing
            api_url = f'https://pub.orcid.org/v3.0/{self._orcid_id}'

        elif self._state == "member":
            # api_url = f'https://api.sandbox.orcid.org/v3.0/{self._orcid_id}'  #for testing
            api_url = f'https://api.orcid.org/v3.0/{self._orcid_id}'

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
        
        access_token = self._orcid_access_token

        # Set the headers with the access token for authentication
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        api_url = ""

        if self._state == "public":
            # Specify the ORCID record endpoint for the desired ORCID iD
            # api_url = f'https://pub.sandbox.orcid.org/v3.0/{self._orcid_id}'  #for testing
            api_url = f'https://pub.orcid.org/v3.0/{self._orcid_id}/{section}'

        elif self._state == "member":
            # api_url = f'https://api.sandbox.orcid.org/v3.0/{self._orcid_id}'  #for testing
            api_url = f'https://api.orcid.org/v3.0/{self._orcid_id}/{section}'

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
        return  : dict with name, biography, researcher-urls
        '''
        data = self.__read_section("person") 
        name = self.__get_value_from_keys(data,["name","given-names", "value"])
        bio = self.__get_value_from_keys(data,["biography", "content"])
        urls = []
        if "researcher-urls" in data and "researcher-url" in data["researcher-urls"]:
            researcher_urls = data["researcher-urls"]["researcher-url"]

            if isinstance(researcher_urls, list):
                for research_url in researcher_urls:
                    url_name = self.__get_value_from_keys(research_url,["url-name"])
                    url_value = self.__get_value_from_keys(research_url,["url","value"])
                    if url_name or url_value:
                        urls.append({"URL Name":url_name,"URL": url_value})

        return {"Name":name,"Bio":bio,"URLs":urls}
    
    def address(self):
        '''
        The researcher's countries or regions
        return  :
        '''
        return self.__read_section("address")  
    
    def email(self):
        '''
        The email address(es) associated with the record
        return  : A tuple of list of emails and whole info tree related to email from orcid
        '''
        data =  self.__read_section("email") 
        emails = [email['email'] for email in self.__get_value_from_keys(data,["person","emails","email"])]
        return emails, data
    
    def external_identifiers(self):
        '''
        Linked external identifiers in other systems
        return  :
        '''
        return self.__read_section("external-identifiers") 
    
    def keywords(self):
        '''
        Keywords related to the researcher and their work
        return  : A tuple of list of keywords and whole info tree related to keywords from orcid
        '''
        data =  self.__read_section("keywords")
        lis = [(value["content"]) for value in data["keyword"]] 

        return (lis, data)
     
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
        return  : a tuple containing the Education details and the whole info tree related to education from orcid
        '''
        data =  self.__read_section("educations") 

        edu = self.__extract_details(data, "education")

        return (edu,data)
    
    def employments(self):
        '''
        Employment affiliations
        return  : a tuple containing the Employment details and the whole info tree related to employment from orcid
        '''
        data =  self.__read_section("employments") 

        employments = self.__extract_details(data, "employment")

        return (employments,data)
    
    def fundings(self):
        '''
        Summary of funding activities
        return  : a tuple containing the Funding details and the whole info tree related to funding from orcid
        '''
        funding_details = []

        data = self.__read_section("fundings") 
        group = data.get('group', [])

        for funding_summary in group:
            funding_summaries = funding_summary.get('funding-summary', [])

            for fund_summary in funding_summaries:
                title       = self.__get_value_from_keys(fund_summary,["title","title","value"])
                fund_type   = self.__get_value_from_keys(fund_summary,["type"])
                start_date  = self.get_formatted_date(fund_summary.get('start-date', {}))
                end_date    = self.get_formatted_date(fund_summary.get('end-date', {}))
                organization= self.__get_value_from_keys(fund_summary,["organization","name"])
                organization_address = ', '.join(filter(None, self.__get_value_from_keys(fund_summary, ["organization", "address"]).values())) if self.__get_value_from_keys(fund_summary, ["organization", "address"]) is not None else ''
                url         = self.__get_value_from_keys(fund_summary,["url","value"])

                funding_detail = {
                    'title': title,
                    'type': fund_type,
                    'start-date': start_date,
                    'end-date': end_date,
                    'organization': organization,
                    'organization-address': organization_address,
                    'url': url,
                }

                funding_details.append(funding_detail)

        return (funding_details,data)
    
    def peer_reviews(self):
        '''
        Summary of peer review activities
        return  :
        '''
        return self.__read_section("peer-reviews") 
    
    def works(self):
        '''
        Summary of research works
        return  : a tuple containing the Work details and the whole info tree related to work from orcid
        '''
        data =  self.__read_section("works") 
        work_details = []

        group = data.get('group', [])

        for work_summary in group:
            work_summaries = work_summary.get('work-summary', [])

            for work_summary in work_summaries:
                title           = self.__get_value_from_keys(work_summary,["title","title","value"])
                work_type       = self.__get_value_from_keys(work_summary,["type"])
                publication_date= self.get_formatted_date(work_summary.get('publication-date', {}))
                journal_title   = self.__get_value_from_keys(work_summary,["journal-title","value"])
                organization    = self.__get_value_from_keys(work_summary,["organization","name"])
                organization_address = ', '.join(filter(None, self.__get_value_from_keys(work_summary, ["organization", "address"]).values())) if self.__get_value_from_keys(work_summary, ["organization", "address"]) is not None else ''
                url             = self.__get_value_from_keys(work_summary,["url","value"])

                work_detail = {
                    'title': title,
                    'type': work_type,
                    'publication-date': publication_date,
                    'journal title': journal_title,
                    'organization': organization,
                    'organization-address': organization_address,
                    'url': url,
                }

                work_details.append(work_detail)

        return (work_details,data)
    
    def research_resources (self):
        '''
        Summary of research resources 
        return  :
        '''
        return self.__read_section("research-resources") 
    
    def services(self):
        '''
        Summary of services 
        return  : a tuple containing the Service details and the whole info tree related to service from orcid
        '''
        data =  self.__read_section("services") 

        services = self.__extract_details(data, "service")

        return (services,data) 
    
    def qualifications(self):
        '''
        Summary of qualifications 
        return  : a tuple containing the Qualification details and the whole info tree related to qualification from orcid
        '''
        data =  self.__read_section("qualifications") 

        qualifications = self.__extract_details(data, "qualification")

        return (qualifications,data)
    
    def memberships(self):
        '''
        Summary of memberships 
        return  : a tuple containing the Membership details and the whole info tree related to membership from orcid
        '''
        data =  self.__read_section("memberships") 

        mem = self.__extract_details(data, "membership")

        return (mem,data)
    
    def distinctions(self):
        '''
        Summary of distinctions 
        return  : a tuple containing the distinction details and the whole info tree related to distinction from orcid
        '''
        data =  self.__read_section("distinctions") 

        distinctions = self.__extract_details(data, "distinction")

        return (distinctions,data)
    
    def invited_positions(self):
        '''
        Summary of invited positions
        return  : a tuple containing the invited position details and the whole info tree related to invited position from orcid
        '''
        data =  self.__read_section("invited-positions") 

        invited_pos = self.__extract_details(data, "invited-position")

        return (invited_pos,data)
    
    def get_formatted_date(self,date_dict):
        """
        Formats a date dictionary into a string (e.g., "MM/YYYY") if all required keys are present and not None.

        Args:
            date_dict (dict): A dictionary containing 'year', 'month', and 'day' keys.

        Returns:
            str: The formatted date string or an empty string if any required key is missing or None.
        """
        if date_dict is not None:
            year = self.__get_value_from_keys(date_dict,["year","value"])
            month = self.__get_value_from_keys(date_dict,["month","value"]) 
            day = self.__get_value_from_keys(date_dict,["day","value"]) 

            # Check if all required keys are present and not None
            if year is not None and month is not None:
                return f"{month}/{year}"
            elif year is not None:
                return year
            else:
                return ''
        else:
            return ''

    def __are_keys_accessible(self,json_obj, keys):
        """
        Check if all keys are accessible cumulatively in the JSON-like object.

        Args:
        json_obj (dict): The JSON-like object (dictionary).
        keys (list): List of keys to check for accessibility.

        Returns:
        bool: True if all keys are accessible cumulatively, False otherwise.
        """
        current_obj = json_obj

        for key in keys:
            if isinstance(current_obj, dict) and key in current_obj:
                current_obj = current_obj[key]
            else:
                return False

        return True

    def __get_value_from_keys(self,json_obj, keys):
        """
        Get the value associated with the last key in the list if all keys are accessible cumulatively.

        Args:
        json_obj (dict): The JSON-like object (dictionary).
        keys (list): List of keys to check for accessibility and retrieve the final value.

        Returns:
        Any: The value associated with the last key if all keys are accessible cumulatively, or None if not accessible.
        """
        if self.__are_keys_accessible(json_obj, keys):
            current_obj = json_obj
            for key in keys:
                current_obj = current_obj[key]
            return current_obj
        else:
            return None
        
    def __extract_details(self, data, key):
        '''
        Helper function for record_summary()
        '''
        details = []
        
        # Extract the 'affiliation-group' from the data
        affiliation_group = data.get('affiliation-group', [])
        
        for group in affiliation_group:
            summaries = group.get('summaries', [])
            
            for summary in summaries:
                key_summary = summary.get(f'{key}-summary', {})
                department  = self.__get_value_from_keys(key_summary,["department-name"])
                role        = self.__get_value_from_keys(key_summary,["role-title"])
                start_date  = self.get_formatted_date(key_summary.get('start-date', {}))
                end_date    = self.get_formatted_date(key_summary.get('end-date', {}))
                organization = self.__get_value_from_keys(key_summary,["organization","name"])
                organization_address = ', '.join(filter(None, self.__get_value_from_keys(key_summary, ["organization", "address"]).values())) if self.__get_value_from_keys(key_summary, ["organization", "address"]) is not None else ''
                url  = self.__get_value_from_keys(key_summary,["url","value"])
                detail = {
                    'Department': department,
                    'Role': role,
                    'start-date': start_date,
                    'end-date': end_date,
                    'organization': organization,
                    'organization-address': organization_address,
                    'url': url,
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
            'Name': self.__get_value_from_keys(data,["person","name","given-names","value"]),
            'Biography': self.__get_value_from_keys(data,["person","biography","content"]),
            'Emails': [email['email'] for email in self.__get_value_from_keys(data,["person","emails","email"])],
            'Research Tags (keywords)': [keyword['content'] for keyword in self.__get_value_from_keys(data,["person","keywords","keyword"])],
        }

        # Extract education details
        education_details = self.educations()[0]
        if education_details: extracted_data['Education'] = education_details

        # Extract education details
        qualification_details = self.qualifications()[0]
        if qualification_details: extracted_data['Quaifications'] = qualification_details

        # Extract employment details
        employment_details = self.employments()[0]
        if employment_details: extracted_data['Employment'] = employment_details

        # Extract education details
        distinction_details = self.distinctions()[0]
        if distinction_details: extracted_data['Distinctions'] = distinction_details

        # Extract employment details
        Invited_details = self.invited_positions()[0]
        if Invited_details: extracted_data['Invited Positions'] = Invited_details

        # Extract education details
        membership_details = self.memberships()[0]
        if membership_details: extracted_data['Memberships'] = membership_details

        # Extract service details
        service_details = self.services()[0]
        if service_details: extracted_data['Service'] = service_details

        # Extract funding details with start and end dates
        extracted_data['Fundings'] = self.fundings()[0]
        extracted_data['Works'] = self.works()[0]

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
    

from orcid import Orcid
import requests
import xmltojson
import json

class OrcidScrapper(Orcid):
    '''
    This is an alternative way to access public data on Orcid website through web-scraping
    Inherited from Orcid class
    '''
    def __init__(self,orcid_id):
        '''
        Initializes the OrcidScrapper class
        '''
        super().__init__(orcid_id)
        return None

    
    def __read_section(self, section="record"):
        '''
        Reads the section of a Orcid member Profile
        return  : a dictionary of summary view of the section of ORCID data 
        '''
        url = f"https://pub.orcid.org/v3.0/{self.orcid_id}/{section}"
        data = self.__orcid_web_scrapper(url)
        print("asfffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        return data[section]
    
    def __orcid_web_scrapper(self,url):
        '''
        Scrape the data from the url (orcid public webpage : pub.orcid.org)
        '''
        xml_data = requests.get(url).content

        #convert the xml tree scraped to a json tree
        json_data = xmltojson.parse(xml_data)
        #json string to json tree
        data = json.loads(json_data)

        #reformat the json tree
        renamed_data = self.__rename_keys(data)
        result = self.__remove_metadata(renamed_data)

        return result
    

    def __rename_keys(self,data):
        '''
        Reformats and renames the keys of a data dictionary acquired 
        thorugh scraping to match the names of keys accessed through API
        return  : a dictionary of summary view of the section of ORCID data'''
        if isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                if ':' in key:
                    _, new_key = key.split(':')
                    new_data[new_key] = self.__rename_keys(value)
                else:
                    new_data[key] = self.__rename_keys(value)
            return new_data
        elif isinstance(data, list):
            return [self.__rename_keys(item) for item in data]
        else:
            return data

    def __remove_metadata(self,data):
        '''
        Removes unnecessary metadata from a data dictionary acquired 
        '''
        result={}
        #section name like record, works, activities-summary
        section = list(data.keys())[0]
        keys_to_remove = list(data[section].keys())[0:30]
        newdata = {key1: data[section][key1] for key1 in data[section] if key1 not in keys_to_remove}
        result[section]=newdata

        return result
    
    
    def __extract_details(self, data, key):
        '''
        Helper function for __read_section to reading various sections for orcid profile
        '''
        details = []
        # Extract the 'affiliation-group' from the data
        affiliation_group = data.get('affiliation-group', [])
        
        for summary in affiliation_group:
                
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

orcid = OrcidScrapper("0000-0003-0666-9883")
print(orcid.generate_markdown_file("scrapper.md"))
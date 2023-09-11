from orcid import Orcid
import requests
from bs4 import BeautifulSoup
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
        self.orcid_id = orcid_id
        return None

    def __orcid_web_scrapper(self,url):
        '''
        Scrape the data from the url (orcid public webpage : pub.orcid.org)
        '''
        xml_data = requests.get(url).content

        soup = BeautifulSoup(xml_data, "xml")

        # Find all text in the data
        texts = str(soup.findAll(text=True)).replace('\\n','')

        json_data = xmltojson.parse(xml_data)
        data = json.loads(json_data)
        
        return data
    
    def __read_section(self, section="record"):
        '''
        Reads the section of a Orcid member Profile
        return  : a dictionary of summary view of the section of ORCID data 
        '''
        url = f"https://pub.orcid.org/{self.orcid_id}/{section}"
        data = self.__orcid_web_scrapper(url)
        return data
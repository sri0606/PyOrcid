from __future__ import annotations

import logging
from typing import Any

import requests
import xmltodict

from .orcid import Orcid

logger = logging.getLogger(__name__)


class OrcidScrapper(Orcid):
    '''
    This is an alternative way to access public data on Orcid website
    through web-scraping
    Inherited from Orcid class
    '''
    def __init__(self, orcid_id: str) -> None:
        """Initialize the OrcidScrapper class.

        Args:
            orcid_id: ORCID ID of the user
        """
        super().__init__(orcid_id)

    def __read_section(self, section="record"):
        '''
        Reads the section of a Orcid member Profile
        return  : a dictionary of summary view of the section of
        ORCID data
        '''
        url = f"https://pub.orcid.org/v3.0/{self._orcid_id}/{section}"
        data = self.__orcid_web_scrapper(url)
        return data[section]

    def __orcid_web_scrapper(self, url: str) -> dict[str, Any]:
        """Scrape data from the ORCID public webpage.

        Args:
            url: URL to scrape data from

        Returns:
            Dictionary containing parsed data

        Raises:
            requests.RequestException: If HTTP request fails
            Exception: If XML parsing fails
        """
        try:
            response = self._session.get(url, timeout=30)
            response.raise_for_status()
            xml_data = response.content

            # Convert the XML tree scraped to a dict
            data = xmltodict.parse(xml_data)
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data from {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to parse XML data: {e}")
            raise

        # reformat the json tree
        renamed_data = self.__rename_keys(data)
        result = self.__remove_metadata(renamed_data)

        return result

    def __rename_keys(self, data):
        '''
        Reformats and renames the keys of a data dictionary acquired
        thorugh scraping to match the names of keys accessed through API
        return  : a dictionary of summary view of the section of
        ORCID data
        '''
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

    def __remove_metadata(self, data):
        '''
        Removes unnecessary metadata from a data dictionary acquired
        '''
        result = {}
        # section name like record, works, activities-summary
        section = list(data.keys())[0]
        keys_to_remove = list(data[section].keys())[0:30]
        newdata = {
            key1: data[section][key1] for key1 in data[section]
            if key1 not in keys_to_remove
        }
        result[section] = newdata

        return result

    def __extract_details(self, data, key):
        '''
        Helper function for __read_section to reading various sections
        for orcid profile
        '''
        details = []
        # Extract the 'affiliation-group' from the data
        affiliation_group = data.get('affiliation-group', [])

        for summary in affiliation_group:

            key_summary = summary.get(f'{key}-summary', {})
            department = self.__get_value_from_keys(
                key_summary, ["department-name"])
            role = self.__get_value_from_keys(
                key_summary, ["role-title"])
            start_date = self.get_formatted_date(
                key_summary.get('start-date', {}))
            end_date = self.get_formatted_date(
                key_summary.get('end-date', {}))
            organization = self.__get_value_from_keys(
                key_summary, ["organization", "name"])
            org_addr_obj = self.__get_value_from_keys(
                key_summary, ["organization", "address"])
            if org_addr_obj is not None:
                organization_address = ', '.join(
                    filter(None, org_addr_obj.values()))
            else:
                organization_address = ''
            url = self.__get_value_from_keys(
                key_summary, ["url", "value"])
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

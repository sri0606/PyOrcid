from __future__ import annotations

import logging
import os
from urllib import parse

import requests

logger = logging.getLogger(__name__)


class OrcidSearch:
    '''
    This is a wrapper class for ORCID Search API
    '''
    def __init__(
        self,
        orcid_access_token: str = " ",
        state: str = "public",
        sandbox: bool = False
    ) -> None:
        """Initialize ORCID search instance.

        Args:
            orcid_access_token: ORCID access token
            state: Whether to use "public" or "member" API of ORCID
            sandbox: Whether to use ORCID sandbox API for testing

        Raises:
            ValueError: If access token is invalid
        """
        self._orcid_access_token = orcid_access_token
        self._state = state
        self._sandbox = sandbox
        self._session = requests.Session()

        # For testing purposes (pytesting on github workflow)
        if orcid_access_token.strip() and orcid_access_token != " ":
            try:
                self.__is_access_token_valid()
            except (KeyError, OSError):
                if not self.__test_is_access_token_valid():
                    raise ValueError(
                        "Invalid access token! Please make sure the "
                        "provided credentials are correct."
                    )

    def search(
        self,
        query,
        start=0,
        rows=1000,
        search_mode="expanded-search",
        columns="orcid,given-names,family-name,"
                "current-institution-affiliation-name"
    ):
        '''
        Search orcid records
        for details on the query format see
        https://info.orcid.org/documentation/api-tutorials/
        api-tutorial-searching-the-orcid-registry/

        query       : the search query
        start       : the offset for the paginated search, default = 0
        rows        : the number of rows to be returned, default = 1000
        search_mode : the search mode, either "expanded-search" (default),
                      "search", or "csv-search"
        columns     : for the csv-search, default:
                      "orcid,given-names,family-name,
                      current-institution-affiliation-name"
        return      : a dictionary of search results
        '''

        access_token = self._orcid_access_token

        _search_mode = "expanded-search"
        if search_mode == "search" or search_mode == "csv-search":
            _search_mode = search_mode
        query_encoded = parse.quote_plus(query)

        api_url = ""

        if self._state == "public":
            # Specify the ORCID record endpoint for the desired ORCID iD
            api_url = 'https://pub.orcid.org/'
            if self._sandbox:
                api_url = 'https://pub.sandbox.orcid.org/'  # for testing

        elif self._state == "member":
            api_url = 'https://api.orcid.org/'
            if self._sandbox:
                api_url = 'https://api.sandbox.orcid.org/'  # for testing

        api_url = (f'{api_url}v3.0/{_search_mode}/?q={query_encoded}'
                   f'&start={start}&rows={rows}')

        content_type = 'application/json'
        if search_mode == "csv-search":
            api_url = api_url + f'&fl={columns}'
            content_type = "text/csv"

        # Set the headers with the access token for authentication
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': content_type
        }

        # Make a GET request to retrieve the ORCID record
        response = requests.get(api_url, headers=headers)

        # The request was successful
        data = response.json()
        # Check the response status code
        if response.status_code == 200 or data is not None:
            return data
        else:
            # Handle the case where the request failed
            print("Failed to retrieve ORCID search results. Status code:",
                  response.status_code)
            return None

    def __is_access_token_valid(self):
        '''
        Checks if the current access token is valid
        '''
        access_token = self._orcid_access_token

        if access_token == "":
            raise ValueError(
                "Empty value for access token! Please make sure you are "
                "authenticated by ORCID as developer.")
        # Make a test request to the API using the token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        api_url = ""

        if self._state == "public":
            # Specify the ORCID record endpoint for the desired ORCID iD
            api_url = 'https://pub.orcid.org/v3.0/search'
            if self._sandbox:
                api_url = 'https://pub.sandbox.orcid.org/v3.0/search'

        elif self._state == "member":
            api_url = 'https://api.orcid.org/v3.0/search'
            if self._sandbox:
                api_url = 'https://api.sandbox.orcid.org/v3.0/search'

        response = requests.get(api_url, headers=headers)

        if response.status_code == 404:
            # The request was successful, and the token is likely valid
            return False
        else:
            # Token may have expired or is invalid
            return True

    # THESE FUNCTIONS ARE FOR TESTING PURPOSES

    def __test_is_access_token_valid(self):
        '''
        FOR TESTING PURPOSES ONLY
        Checks if the current access token is valid
        '''
        # Access the environment variable from github secrets
        access_token = os.environ["ORCID_ACCESS_TOKEN"]
        if access_token == "":
            raise ValueError(
                "Empty value for access token! Please make sure you are "
                "authenticated by ORCID as developer.")
        # Make a test request to the API using the token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        api_url = ""

        if self._state == "public":
            # Specify the ORCID record endpoint for the desired ORCID iD
            api_url = 'https://pub.sandbox.orcid.org/v3.0/search'

        elif self._state == "member":
            api_url = 'https://api.sandbox.orcid.org/v3.0/search'

        response = requests.get(api_url, headers=headers)
        if response.status_code == 404:
            # The request was successful, and the token is likely valid
            return False
        else:
            # Token may have expired or is invalid
            return True

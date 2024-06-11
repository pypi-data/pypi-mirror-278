import requests
import pandas as pd
import json


class MicroService:

    GET_METHOD = 'get'
    POST_METHOD = 'post'
    ERROR_CODES = [500, 502, 504, 429, 400, 403]

    instance = None

    def __init__(self, base_url,user,password,retries=0, timeout=[2000, 5000], backoff_factor=0, requests_args={}):
        """
        Initializes the MicroService object with authentication details and session configuration.

        Args:
            base_url (str): The base URL for the microservice API.
            user (str): Username used for API authentication.
            password (str): Password used for API authentication.
            retries (int): Number of retries for the API requests.
            timeout (list): A list containing the connection timeout and the read timeout.
            backoff_factor (float): The factor to use for determining the delay between retry attempts.
            requests_args (dict): Additional arguments to pass to the requests session.
        """
        self.base_url = base_url
        self.user = user
        self.password = password
        self.retries = retries
        self.timeout = timeout
        self.requests_args = requests_args
        self.backoff_factor = backoff_factor
        self.session = requests.Session()
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-access-tokens': '',
        }

        self.session.headers.update(self.headers)

        MicroService.instance = self

    def _login(self, payload={}):
        """
        Authenticates to the API and updates the session headers with the access token.

        Returns:
            str: The token obtained from the login response.
        """
        try:
            username = self.user
            password = self.password

            login_response = self.session.post(self.base_url + '/login', auth=(username, password))
            token = json.loads(login_response.text)['token']
            self.session.headers['x-access-tokens'] = token
            return token
        except Exception as error:
            print('Login error:', error)

    def _get_data(self, url, method=GET_METHOD, params={}, data={}):
        """
        Fetches data from the API based on the specified method.

        Args:
            url (str): The full API endpoint URL.
            method (str): HTTP method ('get' or 'post').
            params (dict): Parameters to pass in the request.
            data (dict): Data to send in the request (for POST requests).

        Returns:
            dict: Parsed JSON response from the API or raises an exception on error.
        """
        try:
            if 'x-access-tokens' not in self.session.headers or not self.session.headers['x-access-tokens']:
                self._login()
            
            if method == self.POST_METHOD:
                response = self.session.post(url, data=data, params=params)
            else:
                response = self.session.get(url, params=params)

            content_type = response.headers['content-type']

            if response.status_code in [200, 201] and any(
                x in content_type for x in ['application/json', 'application/javascript', 'text/javascript']
            ):
                return response.json()
            else:
                if response.status_code == 429:
                    raise Exception(response.json())
                raise Exception(response.json())
        except Exception as error:
            raise error

    
    def get(self, url='', payload={}):
        """
        Performs a GET request to the specified URL with the provided payload.

        Args:
            url (str): API endpoint extension to the base URL.
            payload (dict): Parameters to pass in the request.

        Returns:
            list or dict: The parsed JSON data received from the API or an empty list on failure.
        """
        req_json = self._get_data(self.base_url + url, self.GET_METHOD, payload)
        if req_json:
            df = req_json
        else:
            df = []
        return df
    
    def post(self, url='', payload={}):
        """
        Performs a POST request to the specified URL with the provided payload.

        Args:
            url (str): API endpoint extension to the base URL.
            payload (dict): Data to send in the POST request.

        Returns:
            list or dict: The parsed JSON data received from the API or an empty list on failure.
        """
        req_json = self._get_data(self.base_url + url, self.POST_METHOD, payload)
        if req_json:
            df = req_json
        else:
            df = []
        return df
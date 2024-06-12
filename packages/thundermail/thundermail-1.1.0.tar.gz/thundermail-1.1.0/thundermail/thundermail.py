# thundermail.py

import os
import requests
import json
from .exceptions import MissingApiKeyError, raise_for_code_and_type

class ThunderMail:
    """
    A Python SDK for interacting with the ThunderMail API.
    The ThunderMail class provides methods for sending and retrieving emails using the ThunderMail API.
    Args:
        key (str, optional): The API key to authenticate requests. If not provided, the key will be retrieved from the THUNDERMAIL_API_KEY environment variable.
    
    Raises:
        MissingApiKeyError: If the API key is missing and not provided in the constructor.
    Attributes:
        base_url (str): The base URL of the ThunderMail API. Defaults to 'https://thundermail.vercel.app/api/v1'.
        headers (dict): The headers to be included in API requests, including the authorization header with the API key.
    Methods:
        send_email(from_email, to, subject, html): Sends an email using the ThunderMail API.
        get_email(email_id): Retrieves an email by its ID using the ThunderMail API.
    """

    def __init__(self, key: (str | None)) -> None:
        self.key = key or os.getenv('THUNDERMAIL_API_KEY')
        if not self.key:
            raise MissingApiKeyError('Missing API key. Pass it to the constructor `ThunderMail("tim_1234567890")`', 'missing_api_key', '401')
        self.base_url = os.getenv('THUNDERMAIL_BASE_URL', 'https://thundermail.vercel.app/api/v1')
        self.headers = {'Authorization': f'Bearer {self.key}'}

    def send(self, from_email, to, subject, html):
        """
        Sends an email using the ThunderMail API.
        Args:
            from_email (str): The email address of the sender.
            to (str or list): The email address(es) of the recipient(s). Can be a single email address or a list of email addresses.
            subject (str): The subject of the email.
            html (str): The HTML content of the email.
        Returns:
            dict: The JSON response from the ThunderMail API.
        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        url = f'{self.base_url}/emails'
        data = {'from': from_email, 'to': to, 'subject': subject, 'html': html}
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise_for_code_and_type(e.response.status_code, e.response.json().get('error', {}).get('type', ''), e.response.json().get('message', ''))
        return response.json()

    def get(self, email_id):
        """
        Retrieves an email by its ID using the ThunderMail API.
        Args:
            email_id (str): The ID of the email to retrieve.
        Returns:
            dict: The JSON response from the ThunderMail API.
        Raises:
            requests.exceptions.HTTPError: If the API request fails.
        """
        url = f'{self.base_url}/emails/{email_id}'
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise_for_code_and_type(e.response.status_code, e.response.json().get('error', {}).get('type', ''), e.response.json().get('message', ''))
        get_response = json.dumps(response.json(), indent=4)
        return get_response
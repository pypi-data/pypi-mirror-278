from .utils.log import log
import requests
import json
import os
from datetime import datetime, timedelta


class Client:
    """
    A class representing a client for interacting with the Consibio Cloud API.

    Attributes:
        _api_url (str, optional): The base URL of the Consibio Cloud API, can be used to override the default URL.
    """
    _api_url = "https://api.v2.consibio.com"

    def __init__(self, api_url=None):
        """
        Initializes a new instance of the Client class.

        Args:
            api_url (str, optional): The base URL of the Consibio Cloud API, can be used to override the default URL.
        """
        if api_url is not None:
            # Strip / if ending with /
            if api_url[-1] == "/":
                api_url = api_url[:-1]

            log.info(f"Setting API URL to {api_url}")
            Client._api_url = api_url

    def get_api_url(self):
        """
        Gets the base URL of the Consibio Cloud API.

        Returns:
            str: The base URL of the Consibio Cloud API.
        """
        return self._api_url

##############################################
# Requests
##############################################

    def http_get(self, url):
        """
        Sends a GET request to the specified URL.

        Args:
            url (str): The URL to send the GET request to.

        Returns:
            dict: The JSON response from the API, or None if an error occurred.
        """
        try:
            response = requests.get(url, headers=self.get_headers())

            data = self.validate_response(response)

            if data is False:
                return None

            return data
        except Exception as e:
            log.error(f"Error occurred during GET request: {e}")
            return None

    def http_post(self, url, payload):
        """
        Sends a POST request to the specified URL with the given payload.

        Args:
            url (str): The URL to send the POST request to.
            payload (dict): The payload to send with the POST request.

        Returns:
            dict: The JSON response from the API, or None if an error occurred.
        """
        try:
            response = requests.post(
                url, json=payload, headers=self.get_headers())

            if self.validate_response(response):
                log.error(
                    f"Error occurred during GET request: {response.text}")
                return None

            return response.json()
        except Exception as e:
            log.error(f"Error occurred during POST request: {e}")
            return None

    def http_patch(self, url, payload):
        """
        Sends a PATCH request to the specified URL with the given payload.

        Args:
            url (str): The URL to send the PATCH request to.
            payload (dict): The payload to send with the PATCH request.

        Returns:
            dict: The JSON response from the API, or None if an error occurred.
        """
        try:
            response = requests.patch(
                url, json=payload, headers=self.get_headers())

            if self.validate_response(response):
                log.error(
                    f"Error occurred during PATCH request: {response.text}")
                return None

            return response.json()
        except Exception as e:
            log.error(f"Error occurred during PATCH request: {e}")
            return None

    def get_headers(self):
        """
        Gets the headers for making API requests.

        Returns:
            dict: The headers for making API requests.
        """
        return {
            "Authorization": f"Bearer {self.auth_login()}"
        }

    def validate_response(self, response):
        """
        Validates the response from an API request.

        Args:
            response (requests.Response): The response object from the API request.

        Returns:
            dict: The JSON data from the response, or None if an error occurred.
        """
        if response.text and response.text == "Unauthenticated":
            # Throw a python error
            raise Exception(
                "Unauthenticated access to the API. Please check your credentials. Login with client.auth_login(username, password), and logout with client.auth_logout().")
        if response.status_code != 200:
            # Try and get the error message
            if "error" in response.json():
                log.error(
                    f"Error occurred during request: {response.json()['error']}")
            else:
                log.error(f"Error occurred during request: {response.text}")
            return None

        data = response.json()
        if "status" in data and data["status"] != "ok":
            # Get the error
            if "payload" in data and "error" in data["payload"]:
                # If text is "Unauthorized or no data found", suggest to try and login again
                if data["payload"]["error"] == "Unauthorized or no data found":
                    log.error(
                        f"Error occurred during request: {data['payload']['error']}. Try and login again, or check if the user has access to the project.")
                else:
                    log.error(
                        f"Error occurred during request: {data['payload']['error']}")
                return None

        if "payload" not in data:
            log.error(f"No payload returned from the API: {data}")
            return None

        return data

##############################################
# Authentication
##############################################

    def auth_logout(self):
        """
        Logs out the user by removing the token file.
        """
        try:
            token_file = "secrets.json"
            if os.path.exists(token_file):
                os.remove(token_file)
        except Exception as e:
            log.error(f"Error occurred during logout: {e}")
            return None

    def auth_login(self, username=None, password=None):
        """
        Logs in the user and returns the access token.

        Args:
            username (str, optional): The username of the user.
            password (str, optional): The password of the user.

        Returns:
            str: The access token, or None if an error occurred.
        """
        try:
            token_file = "secrets.json"
            if os.path.exists(token_file):
                with open(token_file, 'r') as f:
                    token_info = json.load(f)
                    if datetime.now() < datetime.strptime(token_info['expires'], '%Y-%m-%d %H:%M:%S'):
                        return token_info['token']

            # If the token is not valid, then we need to authenticate
            if username is None or password is None:
                log.error(
                    "Username and password are required to authenticate, as the session looks to be invalid/not found.")
                return None

            url = self.get_api_url() + "/login"
            payload = {
                "username": username,
                "password": password
            }
            response = requests.post(url, json=payload)

            if response.status_code != 200:
                log.error(
                    f"Error occurred during authentication: {response.text}")
                return None

            if "payload" not in response.json():
                log.error(
                    f"Error occurred during authentication: {response.text}")
                return None

            if "token" not in response.json()["payload"]:
                log.error(
                    f"Error occurred during authentication: {response.text}")
                return None

            access_token = response.json()["payload"]["token"]
            # Assuming the token expires in 1 hour
            expires = (datetime.now() + timedelta(hours=1)
                       ).strftime('%Y-%m-%d %H:%M:%S')

            with open(token_file, 'w') as f:
                json.dump({'token': access_token, 'expires': expires}, f)

            return access_token
        except Exception as e:
            log.error(f"Error occurred during authentication: {e}")
            return None

    def auth_valid(self):
        """
        Checks if the user is authenticated.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        try:
            token_file = "secrets.json"
            if os.path.exists(token_file):
                with open(token_file, 'r') as f:
                    token_info = json.load(f)
                    if datetime.now() < datetime.strptime(token_info['expires'], '%Y-%m-%d %H:%M:%S'):
                        return True
            return False
        except Exception as e:
            log.error(f"Error occurred during authentication validation: {e}")
            return False

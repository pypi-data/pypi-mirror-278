
#Python Imports
import requests

#Django Imports

#Third-Party Imports
from decouple import config

#Project-Specific Imports
from properties import ADMIN_IDENTIFER

#Relative Import



def get_environment_host():
    """Get the environment host"""
    return config('ENVIRONMENT_HOST')

def get_environment_port():
    """Get the environment port"""
    return config('ENVIRONMENT_PORT')



def get_access_token(username='BrightSky23', password='B3autifulD@y$'):
    """
    Obtain an access token using the provided username and password.

    Args:
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        str: The obtained access token, or None if authentication fails.
    """
    host = get_environment_host()
    port = get_environment_port()
    
    auth_url = f'http://{host}:{port}/auth/pass/'

    # Payload for authentication
    auth_payload = {
        'username': username,
        'password': password,
    }
    
    headers = {'Tenant-Identifier': "admin"}

    try:
        # Make the HTTP POST request to obtain the token
        auth_response = requests.post(auth_url, data=auth_payload,headers=headers)

        if auth_response.status_code == 200:
            # Extract the access token from the response
            access_token = auth_response.json().get('access_token')
            return access_token
        else:
            return auth_response

    except requests.exceptions.RequestException as e:
        print(f'Error during authentication: {e}')
        return None



# class MicroserviceClient:
#     """A client for interacting with a microservice via HTTP POST requests."""

#     def __init__(self, tenant_identifier='admin', token=None):
#         """Initialize the MicroserviceClient instance."""
#         self.tenant_identifier = tenant_identifier
#         self.token = token or self.get_default_token()
#         self.host = self.get_default_host()
#         self.port = self.get_default_port()

#     def get_default_token(self):
#         """Obtain the default access token."""
#         return get_access_token()

#     def post(self, endpoint, data=None, params=None):
#         """Make an HTTP POST request to the specified endpoint."""
#         url = f'http://{self.host}:{self.port}/{endpoint}'
#         headers = {'Authorization': f'Bearer {self.token}', "Tenant-Identifier": self.tenant_identifier}
#         response = requests.post(url, json=data, headers=headers, params=params)
#         # Raise an exception for bad responses (4xx or 5xx)
#         # response.raise_for_status()
#         return response.json()

#     def patch(self, endpoint, data=None, params=None):
#         """Make an HTTP POST request to the specified endpoint."""
#         url = f'http://{self.host}:{self.port}/{endpoint}'
#         headers = {'Authorization': f'Bearer {self.token}', "Tenant-Identifier": self.tenant_identifier}
#         response = requests.patch(url, json=data, headers=headers, params=params)
#         # Raise an exception for bad responses (4xx or 5xx)
#         # response.raise_for_status()
#         return response.json()

#     def put(self, endpoint, data=None, params=None):
#         """Make an HTTP POST request to the specified endpoint."""
#         url = f'http://{self.host}:{self.port}/{endpoint}'
#         headers = {'Authorization': f'Bearer {self.token}', "Tenant-Identifier": self.tenant_identifier}
#         response = requests.put(url, json=data, headers=headers, params=params)
#         # Raise an exception for bad responses (4xx or 5xx)
#         # response.raise_for_status()
#         return response.json()

#     def get_default_host(self):
#         """Obtain the default host for the microservice."""
#         return get_enviroment_host()

#     def get_default_port(self):
#         """Obtain the default port for the microservice."""
#         return get_enviroment_port()

#     def build_url(self, endpoint):
#         """Build the complete URL for a given endpoint."""
#         return f'http://{self.host}:{self.port}/{endpoint}'

#     def build_headers(self):
#         """Build the headers for an HTTP request."""
#         return {
#             'Authorization': f'Bearer {self.token}',
#             'Tenant-identifier': self.tenant_identifier
#         }




class MicroserviceClient:
    """A client for interacting with a microservice via HTTP requests."""

    def __init__(self, tenant_identifier=ADMIN_IDENTIFER, token=None):
        """Initialize the MicroserviceClient instance."""
        self.tenant_identifier = tenant_identifier
        self.token = token or self.get_default_token()
        self.base_url = self.build_base_url()

    def get_default_token(self):
        """Obtain the default access token."""
        return get_access_token()

    def make_request(self, method, endpoint, data=None, params=None):
        """Make an HTTP request to the specified endpoint with the given method."""
        url = f'{self.base_url}/{endpoint}'
        headers = self.build_headers()
        request_method = getattr(requests, method.lower())
        response = request_method(url, json=data, headers=headers, params=params)
        # Raise an exception for bad responses (4xx or 5xx)
        # response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None, params=None):
        """Make an HTTP POST request to the specified endpoint."""
        return self.make_request('POST', endpoint, data=data, params=params)

    def get(self, endpoint, params=None):
        """Make an HTTP GET request to the specified endpoint."""
        return self.make_request('GET', endpoint, params=params)

    def patch(self, endpoint, data=None, params=None):
        """Make an HTTP PATCH request to the specified endpoint."""
        return self.make_request('PATCH', endpoint, data=data, params=params)

    def put(self, endpoint, data=None, params=None):
        """Make an HTTP PUT request to the specified endpoint."""
        return self.make_request('PUT', endpoint, data=data, params=params)

    def build_base_url(self):
        """Build the base URL for the microservice."""
        return f'http://{self.get_default_host()}:{self.get_default_port()}'

    def get_default_host(self):
        """Obtain the default host for the microservice."""
        return get_environment_host()

    def get_default_port(self):
        """Obtain the default port for the microservice."""
        return get_environment_port()

    def build_headers(self):
        """Build the headers for an HTTP request."""
        return {
            'Authorization': f'Bearer {self.token}',
            'Tenant-Identifier': self.tenant_identifier
        }


from swift_behaviors import ObjectStorageAPI_Behaviors
from os_client import ObjectStorageAPIClient
from swift_config import ObjectStorageAPIConfig, ObjectStorageConfig, UserAuthConfig, UserConfig

import json
import os

from behest.client import HTTPClient


class ObjectStorageComposite(object):
    """
    Handles authing and retrieving the storage_url and auth_token for
    storage objects.
    """

    def __init__(self):

        def authenticate(url, username, api_key):
            client = HTTPClient()
            content = {"auth": {"RAX-KSKEY:apiKeyCredentials": {"username": username, "apiKey": api_key}}}
            body = json.dumps(content)
            response = client.request("POST", url + '/v2.0/tokens', data=body, headers={'Content-type': 'application/json'})

            return response

        config_file_path = os.environ['TEST_CONFIG']
        user_auth_config = UserAuthConfig(
            config_file_path=config_file_path,
            section_name=UserAuthConfig.SECTION_NAME)
        
        user_config = UserConfig(
            config_file_path=config_file_path,
            section_name=UserConfig.SECTION_NAME)

        obj_storage_config = ObjectStorageConfig()

        r = authenticate(
            url=user_auth_config.auth_endpoint,
            username=user_config.username,
            api_key=user_config.api_key)

        services = r.json()['access']['serviceCatalog']

        swift_service = [service for service in services if service['name'] == obj_storage_config.identity_service_name]
        swift_service = swift_service[0]
        swift_endpoint = [endpoint for endpoint in swift_service['endpoints'] if endpoint['region'] == obj_storage_config.region]

        self.storage_url = swift_endpoint[0]['publicURL']
        self.auth_token =  r.json()['access']['token']['id']

        self.config = ObjectStorageAPIConfig(
            config_file_path=config_file_path,
            section_name=ObjectStorageAPIConfig.SECTION_NAME)

        # self.config = ObjectStorageAPIConfig()

        self.client = ObjectStorageAPIClient(self.storage_url, self.auth_token)

        self.behaviors = ObjectStorageAPI_Behaviors(
            client=self.client, config=self.config)
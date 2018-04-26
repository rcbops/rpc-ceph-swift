import json

from behest.client import HTTPClient

from swift_silent_deadly.os_client import ObjectStorageAPIClient
from swift_silent_deadly.swift_config import ObjectStorageAPIConfig
from swift_silent_deadly.swift_behaviors import ObjectStorageAPI_Behaviors

def authenticate(url, username, api_key):
    client = HTTPClient()
    content = {"auth": {"RAX-KSKEY:apiKeyCredentials": {"username": username, "apiKey": api_key}}}
    body = json.dumps(content)
    response = client.request("POST", url, data=body, headers={'Content-type': 'application/json'})
    return response

url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
r = authenticate(url=url, username='dwnova', api_key='aab8017a4a644a0fa1972959b0f1b06f')

services = r.json()['access']['serviceCatalog']

swift_service = [service for service in services if service['name'] == 'cloudFiles']
swift_service = swift_service[0]
swift_endpoint = [endpoint for endpoint in swift_service['endpoints'] if endpoint['region'] == 'DFW']
endpoint = swift_endpoint[0]['publicURL']
token =  r.json()['access']['token']['id']

client = ObjectStorageAPIClient(storage_url=endpoint, auth_token=token)
config = ObjectStorageAPIConfig(
    config_file_path='dfw.config',
    section_name=ObjectStorageAPIConfig.SECTION_NAME)
behavior = ObjectStorageAPI_Behaviors(client=client, config=config)
print behavior.get_swift_features()



#curl https://identity.api.rackspacecloud.com/v2.0/tokens -X POST -d '{"auth":{"RAX-KSKEY:apiKeyCredentials":{"username":"dwnova","apiKey":"aab8017a4a644a0fa1972959b0f1b06f"}}}' -H "Content-type: application/json"

#{"auth":{"RAX-KSKEY:apiKeyCredentials":{"username":"dwnova","apiKey":"aab8017a4a644a0fa1972959b0f1b06f"}}}
#{"auth":{"RAX-KSKEY: apiKeyCredentials": {"username": "dwnova", "apiKey": "aab8017a4a644a0fa1972959b0f1b06f"}}}
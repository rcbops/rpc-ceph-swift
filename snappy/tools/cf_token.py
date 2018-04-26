#!/usr/bin/python
import argparse
import json
import urllib3
import sys


parser = argparse.ArgumentParser()
parser.add_argument("--user", dest='usr')
parser.add_argument("--password", dest='pwd')
parser.add_argument("--api_key", dest='key')
parser.add_argument("--internal", action="store_true")
args = parser.parse_args()

headers = {'Content-Type': 'application/json'}
body = {}
url = ""
data = ""

if args.pwd:
    body = { 'auth':{'passwordCredentials':{'username':args.usr, 'password':args.pwd}}}
elif args.key:
    body = {'auth':{'RAX-KSKEY:apiKeyCredentials':{'username':args.usr,'apiKey':args.key}}}
else:
    print args.pwd
    print args.key
    sys.exit(-1)

if args.internal:
    url = 'https://staging.identity-internal.api.rackspacecloud.com/v2.0/tokens'
else:
    url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'

print "\nAuth URL: " + url

urllib3.disable_warnings()
http = urllib3.PoolManager(cert_reqs='CERT_NONE')
rsp = http.urlopen(
    'POST',
    url,
    headers=headers,
    body=json.dumps(body))

if rsp.status != 200:
    print rsp.data
    print args
else:
    data = rsp.data

if len(data) > 0:
    data_json = json.loads(data)

    # service catalog
    service_catalog = data_json["access"]["serviceCatalog"]


    # endpoints
    if service_catalog:
        print "=-" * 80
        for thing in service_catalog:
            if thing['name'] == 'cloudFiles':
                print "Service Name: " + thing['name']
                print "Type: " + thing['type']
                for bokko in thing['endpoints']:
                    print "\n"
                    print "Region: " + bokko['region']
                    print "Public URL: " + bokko['publicURL']
                    print "Internal URL: " + bokko['internalURL']
                break

    if data_json.has_key('access'):
       tenant_id = data_json['access']['token']['tenant']['id']
       token = data_json['access']['token']['id']
       print "=-"*80
       print "Tenant ID:"
       print tenant_id
       print "\nToken:"
       print token
    else:
       print data



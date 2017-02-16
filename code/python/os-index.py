#!/usr/bin/env python

import httplib
import json
import argparse
import re
import ssl

parser = argparse.ArgumentParser(description='Return a comma-separated list of OS Families and their corresponding ID')
parser.add_argument('--target-url', required=True, help='URL for the UpGuard instance. This should be the hostname only (appliance.upguard.org instead of https://appliance.upguard.org)')
parser.add_argument('--api-key', required=True, help='API key for the UpGuard instance')
parser.add_argument('--secret-key', required=True, help='Secret key for the UpGuard instance')
parser.add_argument('--insecure', action='store_true', help='Ignore SSL certificate checks')

args = parser.parse_args()

# Initialization
url = args.target_url
if 'http' in url:
    # URL needs to be a hostname, so remove 'https://'
    re.sub('https?:\/\/', '', url)

try:
    browser = httplib.HTTPConnection(url)
    if args.insecure:
        context = ssl._create_unverified_context()
        browser = httplib.HTTPSConnection(args.target_url, context=context)
    browser.request("GET", "/api/v1/operating_systems.json", '',
        {"Authorization": 'Token token="' + args.api_key + args.secret_key + '"',
        "Accept": "application/json"})
    res = browser.getresponse()
    # read() must be called before close(), or it will return an empty string
    data = res.read()

    if res.status == 301:
        raise httplib.HTTPException(
            "Returned {}, try running script with `--insecure` argument".format(res.status))
    elif res.status >= 400:
        raise httplib.HTTPException(
            "{} {}\n{}".format(
                str(res.status),
                res.reason,
                (data.strip() if data else 'No Data Returned')))

    browser.close()

    if data != '':
        print "{},{},{}".format(
            'Operating System',
            'ID',
            'Operating System Family ID')
        for i in json.loads(data):
            print "{},{},{}".format(
                i['description'], i['id'], i['operating_system_family_id'])
    else:
        print str(res.status) + res.reason
except httplib.HTTPException as h:
    print h.message
finally:
    browser.close()

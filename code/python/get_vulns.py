import httplib
import json

api_key = 'your api key'
secret_key = 'your secret key'
url = 'appliance url here'
filename = 'vuln.log'

try:
  browser = httplib.HTTPConnection(url)
  # -- For HTTPS connections
  # context = ssl._create_unverified_context()
  # browser = httplib.HTTPSConnection(url, context=context)
  get_headers = {"Authorization": 'Token token="' + api_key + secret_key + '"',
  "Accept": "application/json"}
  browser.request("GET", "/api/v2/vulns.json?reported=month", '', get_headers)
  get_res = browser.getresponse()
  # read() must be called before close(), or it will return an empty string
  data = get_res.read()
  print data
  vulns = []
  # vulns = json.load(data)
  # f = open('file', 'w')
  for vuln in vulns:
    line = ''
    # append vuln attributes into line
    # ...
    # write line to file
    # print vuln
  if get_res.status >= 400:
      raise httplib.HTTPException(str(get_res.status) + ' ' +
          get_res.reason + (': ' + data.strip() if data.strip() else ''))
  else:
      print str(get_res.status) + get_res.reason;
except httplib.HTTPException as h:
  print h.message
finally:
  browser.close()


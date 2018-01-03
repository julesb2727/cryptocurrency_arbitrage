import urllib.request as urllib2
base_url = "https://api.gemini.com/v1"
# or, for sandbox
# base_url = "https://api.sandbox.gemini.com/v1"
response = urllib2.urlopen(base_url + "/pubticker/btcusd")
print(response.read())

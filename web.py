import urllib.request as urllib2


url = "http://www.google.com"
headers = {}
headers['User-Agent'] = "Googlebot"
request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)
print(response.read())
response.close()

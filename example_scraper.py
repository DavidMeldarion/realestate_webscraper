from bs4 import BeautifulSoup
from requests import get
import certifi
import urllib3
from urllib.request import Request, urlopen
import pandas as pd
import csv

#creating arrays
addresses = []
beds = []
baths = []
size = []
prices = []
urls = []
description = []

#setting up secure HTTPS Requests from https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

#Defining URL to scrape (replace example.com with your website)
url = 'https://www.example.com/city/30794/TX/Dallas/filter/property-type=house,max-price=200k'
#Defining User-Agent to impersonate browser from https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
headers = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})

#Getting URL for BeautifulSoup
response = Request(url, headers=headers)
webpage = urlopen(response).read()
content = BeautifulSoup(webpage, "html.parser")

#For loop to iterate through page
for house in content.findAll('div', attrs={"class" : "HomeCardContainer"}):
	
	price=house.findAll('span', attrs={"class" : "homecardV2Price"})[0].text
	prices.append(price)
	
	address=house.findAll('span',attrs={"data-rf-test-id" : "abp-streetLine"})[0].text
	addresses.append(address)
	
	bed=house.findAll('div', attrs={"class" : "stats"})[0].text
	beds.append(bed)

	bath=house.findAll('div', attrs={"class" : "stats"})[1].text
	baths.append(bath)

	sqft=house.findAll('div', attrs={"class" : "stats"})[2].text
	size.append(sqft)

	describe=house.findAll('div', attrs={"class" : "remarks-copy"})
	description.append(describe)

	link=house.findAll('a', attrs={"data-rf-test-name" : "basic-card-photo"})[0]
	urls.append('https://www.example.com' + link.get('href'))

print(response)

cols = ['Prices', 'Addresses', 'Beds', 'Baths', 'Size', 'Description', 'URL']

Dallas = pd.DataFrame({"Price" : prices,
						"Address" : addresses,
						"Beds" : beds,
						"Baths" : baths,
						"Size" : size,
						"Description" : description,
						"URL" : urls,
	})

Dallas.to_csv('Dallas_raw.csv')

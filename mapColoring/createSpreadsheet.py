import requests
import json
import pandas as pd
# get data on name, region, 3 letter code, neighboring countries
response = requests.get('https://restcountries.eu/rest/v2/all?fields=name;region;alpha3Code;borders')
if response:
    print('Success!')
    myCountriesDict = response.json()
    myCountries = []
    fullInfo = []
    # filter countries for asian countries
    for item in myCountriesDict:
    	if(item['region'] == "Asia"):
    		myCountries.append(item)
    for item in myCountries:
    	curr= []
    	curr.append(item["name"])
    	Neighbors = ""
    	# merge all  neighbouring countries
    	for elem in myCountries:
    		for border in item["borders"]:
    			if border == elem["alpha3Code"]:
    				Neighbors = Neighbors + "," + elem["name"]
    	curr.append(Neighbors)
    	fullInfo.append(curr)
    print(fullInfo)
    # use pandas to write the info to excel file
    dfObj = pd.DataFrame(fullInfo, columns = ['Name', 'Neighbors'])
    dfObj.to_excel('./input.xlsx')
else:
    print('An error has occurred.')
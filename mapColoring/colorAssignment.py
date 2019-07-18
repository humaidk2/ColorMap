import pandas as pd
import numpy as np
import random
import requests
import json
# get data on name, region, 3 letter code, neighboring countries

class colorAssignment:
    def neighborSort(self, elem):
        return len(elem["borders"])
    def __init__(self, continent):
        self.numOfNodes = 1
        self.numOfNodesDeleted = 0
        self.numOfTimesBackTracking = 0
        response = requests.get('https://restcountries.eu/rest/v2/all?fields=name;region;alpha2Code;alpha3Code;borders')
        if response:
            print('Success!')
            myCountriesDict = response.json()
            myCountries = []
            fullInfo = []
            self.countriesList = []
            self.neighbors = []
            self.alphaCode = []
            self.colors = []
            # filter countries for asian countries
            for item in myCountriesDict:
                if(item['region'] == continent):
                    myCountries.append(item)
            myCountries.sort(key=self.neighborSort, reverse=True)
            for item in myCountries:
                self.countriesList.append(item["name"].replace(",",""))
                print(item["name"].replace(",",""))
                Neighbors = ""
                # merge all  neighbouring countries
                for elem in myCountries:
                    for border in item["borders"]:
                        if border == elem["alpha3Code"]:
                            Neighbors = Neighbors + "," + elem["name"].replace(",","")
                self.neighbors.append(Neighbors)
                self.alphaCode.append(item["alpha2Code"])
            self.countries = []
        else:
            print('An error has occurred.')
    
# format for each country
#   countries = {"india": { "neighbors": ["pakistan", "bangladesh", "nepal"], "options": ["red", "green", "blue"], "color": 'orange', "isAssigned": True}, "pakistan": {"neighbors": ["india", "bla"], "options": [ "green", "blue"], "isAssigned": False}}
    def formatInput(self, numOfCOlors):
        for idx,country in enumerate(self.countriesList):
            currCountry = {}
            currCountry["name"] = country
            neighborList = self.neighbors[idx].encode('utf-8').split(",")
            del neighborList[0]
            currCountry["neighbors"]= neighborList
            currCountry["options"] = [i for i in range(int(numOfCOlors))]
            currCountry["assigned"] = False
            self.countries.append(currCountry)

    def searchForCountry(self, countryName):
        for idx, country in enumerate(self.countries):
            if(country["name"] == countryName or country["name"] == countryName.decode('utf-8')):
                return idx
# return false(try anothe color) if theres any conflicts in the assigned colors
# return false(try anothe color)  if any options are empty(no option available)(conflict)
# return true if all colors have successfully assigned
# assign a color to any unassigned country
# remove that color from neighbours and recurse
# return true if recursion succeeds
# try next color if recursion fails
# return false if no other options left
    def recursive(self, countries):
        # check if any color options are empty
        numOfAssigned = 0
        for country in countries:
            # check for conflicting options for assigned countries and their neghbours
            if country["assigned"] == True:
                for neighbor in country["neighbors"]:
                    if countries[self.searchForCountry(neighbor)]["assigned"] == True:
                        if countries[self.searchForCountry(neighbor)]["color"] == country["color"]:
                            return False
                numOfAssigned += 1
            # if countries no options are available for a country return its not possible 
            else: 
                if len(country["options"]) == 0:
                    return False
        # check if all color options have been assigned return that we're done
        if numOfAssigned == len(countries):
            return True
        else:
            # select next unassigned country and assign it
            for countryIndex, country in enumerate(countries):
                if country["assigned"] == False:
                    currCountryIndex = countryIndex
                    country["assigned"] = True
                    break
            # for every possible color option for this unassigned country color
            for option in countries[currCountryIndex]["options"]:
                # used for backtracking to store any options we delete
                deletedOptions = []
                # set the color to the current option
                countries[currCountryIndex]["color"] = option
                # remove all the options from the neighbors and 
                # store the removed neighbor in deletedOptions
                for neighbor in countries[currCountryIndex]["neighbors"]:
                    if countries[currCountryIndex]["color"] in countries[self.searchForCountry(neighbor)]["options"]:
                        deletedOptions.append(self.searchForCountry(neighbor))
                        countries[self.searchForCountry(neighbor)]["options"].remove(option)
                        self.numOfNodesDeleted += 1
                # recurse to the next variable
                checkIfFinished = self.recursive(countries)
                self.numOfNodes += 1
                # check if all colors were succesfully assigned
                if checkIfFinished == True:
                    return True
                # if colors werent assigned
                # re-assign the deleted colors
                # deleted the current color
                else:
                    for deletedOption in deletedOptions:
                        countries[deletedOption]["options"].append(countries[currCountryIndex]["color"])
                self.numOfTimesBackTracking += 1
            countries[currCountryIndex]["assigned"] = False
            del countries[currCountryIndex]["color"]
            return False

    def runModule(self):
        print("*****************\n\n\n\n\n\n*****************\n")
        isItPossible = self.recursive(self.countries)
        if isItPossible == True:
            finalOutput = []
            for country in self.countries:
                if(country["color"] == 0):
                    country["color"] = "red"
                elif(country["color"] == 1):
                    country["color"] = "blue"
                elif(country["color"] == 2):
                    country["color"] = "green"
                elif(country["color"] == 3):
                    country["color"] = "purple"
                elif(country["color"] == 4):
                    country["color"] = "yellow"
                elif(country["color"] == 5):
                    country["color"] = "pink"
                elif(country["color"] == 6):
                    country["color"] = "brown"
                elif(country["color"] == 7):
                    country["color"] = "orange"
                self.colors.append(country["color"])
                finalOutput.append([country, country["neighbors"], country["assigned"], country["color"]])
                # df = pd.DataFrame(finalOutput, columns=['country','neighbors', 'assigned', 'color'])
            return {
                'countries': self.countriesList,
                'neighbors': self.neighbors,
                'colors': self.colors,
                'alpha2Code': self.alphaCode,
                'stats': {
                    'numOfNodes': self.numOfNodes,
                    'numOfNodesDeleted' : self.numOfNodesDeleted,
                    'numOfTimesBackTracking' : self.numOfTimesBackTracking
                }
            }
        else:
            return {'stats': {
                    'numOfNodes': self.numOfNodes,
                    'numOfNodesDeleted' : self.numOfNodesDeleted,
                    'numOfTimesBackTracking' : self.numOfTimesBackTracking
                    }
                }

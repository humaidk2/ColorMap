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
                self.countriesList.append(item["name"])
                Neighbors = ""
                # merge all  neighbouring countries
                for elem in myCountries:
                    for border in item["borders"]:
                        if border == elem["alpha3Code"]:
                            Neighbors = Neighbors + "," + elem["name"]
                self.neighbors.append(Neighbors)
                self.alphaCode.append(item["alpha2Code"])
            self.countries = {}
        else:
            print('An error has occurred.')
    
# format for each country
#   countries = {"india": { "neighbors": ["pakistan", "bangladesh", "nepal"], "options": ["red", "green", "blue"], "color": 'orange', "isAssigned": True}, "pakistan": {"neighbors": ["india", "bla"], "options": [ "green", "blue"], "isAssigned": False}}
    def formatInput(self, numOfCOlors):
        for idx,country in enumerate(self.countriesList):
            self.countries[country] = {}
            neighborList = str(self.neighbors[idx]).split(",")
            del neighborList[0]
            self.countries[country]["neighbors"]= neighborList
            self.countries[country]["options"] = [i for i in range(int(numOfCOlors))]
            self.countries[country]["assigned"] = False


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
            if countries[country]["assigned"] == True:
                for neighbor in countries[country]["neighbors"]:
                    if countries[neighbor]["assigned"] == True:
                        if countries[neighbor]["color"] == countries[country]["color"]:
                            return False
                numOfAssigned += 1
            # if countries no options are available for a country return its not possible 
            else: 
                if len(countries[country]["options"]) == 0:
                    return False
        # check if all color options have been assigned return that we're done
        if numOfAssigned == len(countries):
            return True
        else:
            # select next unassigned country and assign it
            for country in countries:
                if countries[country]["assigned"] == False:
                    currCountry = country
                    countries[currCountry]["assigned"] = True
                    break
            # for every possible color option for this unassigned country color
            for option in countries[currCountry]["options"]:
                # used for backtracking to store any options we delete
                deletedOptions = []
                # set the color to the current option
                countries[currCountry]["color"] = option
                # remove all the options from the neighbors and 
                # store the removed neighbor in deletedOptions
                for neighbor in countries[currCountry]["neighbors"]:
                    if countries[currCountry]["color"] in countries[neighbor]["options"]:
                        deletedOptions.append(neighbor)
                        countries[neighbor]["options"].remove(option)
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
                        countries[deletedOption]["options"].append(countries[currCountry]["color"])
                self.numOfTimesBackTracking += 1
            countries[currCountry]["assigned"] = False
            del countries[currCountry]["color"]
            return False

    def runModule(self):
        print("*****************\n\n\n\n\n\n*****************\n")
        isItPossible = self.recursive(self.countries)
        if isItPossible == True:
            finalOutput = []
            for country in self.countries:
                if(self.countries[country]["color"] == 0):
                    self.countries[country]["color"] = "red"
                elif(self.countries[country]["color"] == 1):
                    self.countries[country]["color"] = "blue"
                elif(self.countries[country]["color"] == 2):
                    self.countries[country]["color"] = "green"
                elif(self.countries[country]["color"] == 3):
                    self.countries[country]["color"] = "purple"
                elif(self.countries[country]["color"] == 4):
                    self.countries[country]["color"] = "yellow"
                elif(self.countries[country]["color"] == 5):
                    self.countries[country]["color"] = "pink"
                elif(self.countries[country]["color"] == 6):
                    self.countries[country]["color"] = "brown"
                elif(self.countries[country]["color"] == 7):
                    self.countries[country]["color"] = "orange"
                self.colors.append(self.countries[country]["color"])
                finalOutput.append([country, self.countries[country]["neighbors"], self.countries[country]["assigned"], self.countries[country]["color"]])
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

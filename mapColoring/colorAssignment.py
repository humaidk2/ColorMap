import pandas as pd
import numpy as np
import random
import requests
import json
# get data on name, region, 3 letter code, neighboring countries

class colorAssignment:
    def __init__(self):
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
           
            df = pd.DataFrame(fullInfo, columns = ['Name', 'Neighbors'])
            self.countriesList = df.iloc[:,0].tolist()
            self.neighbors = df.iloc[:, 1].tolist()
            self.countries = {}

        else:
            print('An error has occurred.')
    
  
# format for each country
#  india: { neighbors: [pakistan, bangladesh, nepal], color: 'orange'}, pakistan: {neighbors: [india, bla], color: 'red'}
    def formatInput(self):
        for idx,country in enumerate(self.countriesList):
            self.countries[country] = {}
            neighborList = str(self.neighbors[idx]).split(",")
            del neighborList[0]
            self.countries[country]["neighbors"]= neighborList
            self.countries[country]["options"] = [i for i in range(5)]
            self.countries[country]["assigned"] = False
# have an evaluation function
# to check number of conflicts
# fix one conflict
# re-evaluate number of conflicts
# if theres an improvement check next conflict
# if theres no improvement go back and try assigning it to another color


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
                # recurse to the next variable
                checkIfFinished = self.recursive(countries)
                # check if all colors were succesfully assigned
                if checkIfFinished == True:
                    return True
                # if colors werent assigned
                # re-assign the deleted colors
                # deleted the current color
                else:
                    for deletedOption in deletedOptions:
                        countries[deletedOption]["options"].append(countries[currCountry]["color"])
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
                elif(countries[country]["color"] == 1):
                    self.countries[country]["color"] = "blue"
                elif(self.countries[country]["color"] == 2):
                    self.countries[country]["color"] = "green"
                elif(self.countries[country]["color"] == 3):
                    self.countries[country]["color"] = "purple"
                elif(self.countries[country]["color"] == 4):
                    self.countries[country]["color"] = "yellow"
                finalOutput.append([country, self.countries[country]["neighbors"], self.countries[country]["assigned"], self.countries[country]["color"]])
                # df = pd.DataFrame(finalOutput, columns=['country','neighbors', 'assigned', 'color'])
                return finalOutput
        else:
            return []

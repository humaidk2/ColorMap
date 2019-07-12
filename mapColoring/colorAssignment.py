import pandas as pd
import numpy as np
import random

class colorAssignment:
	
    df = pd.read_excel('input.xlsx')
    countriesList = df.iloc[:,1].tolist()
    neighbors = df.iloc[:, 2].tolist()
    countries = {}
# format for each country
#  india: { neighbors: [pakistan, bangladesh, nepal], color: 'orange'}, pakistan: {neighbors: [india, bla], color: 'red'}
def formatInput():
	for idx,country in enumerate(countriesList):
		countries[country] = {}
		neighborList = str(neighbors[idx]).split(",")
		del neighborList[0]
		countries[country]["neighbors"]= neighborList
		countries[country]["options"] = [i for i in range(5)]
		countries[country]["assigned"] = False
# have an evaluation function
# to check number of conflicts
# fix one conflict
# re-evaluate number of conflicts
# if theres an improvement check next conflict
# if theres no improvement go back and try assigning it to another color


def recursive(countries):
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
			checkIfFinished = recursive(countries)
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
def runModule():
	print("*****************\n\n\n\n\n\n*****************\n")
	isItPossible = recursive(countries)
	if isItPossible == True:
		return "Yeah it's possible"
		finalOutput = []
		for country in countries:
			if(countries[country]["color"] == 0):
				countries[country]["color"] = "red"
			elif(countries[country]["color"] == 1):
				countries[country]["color"] = "blue"
			elif(countries[country]["color"] == 2):
				countries[country]["color"] = "green"
			elif(countries[country]["color"] == 3):
				countries[country]["color"] = "purple"
			elif(countries[country]["color"] == 4):
				countries[country]["color"] = "yellow"
			finalOutput.append([country, countries[country]["neighbors"], countries[country]["assigned"], countries[country]["color"]])

		df = pd.DataFrame(finalOutput, columns=['country','neighbors', 'assigned', 'color'])
		df.to_excel("output.xlsx")
	else:
		return "Damn Not possible"

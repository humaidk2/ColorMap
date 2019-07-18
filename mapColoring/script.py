from colorAssignment import colorAssignment
import sys

def script(continent = "World", nColors = 7):
	ca = colorAssignment(continent)
	ca.formatInput(nColors)
	return ca.runModule()
print(script(sys.argv[1], sys.argv[2]))
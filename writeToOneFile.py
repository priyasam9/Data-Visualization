import sys
import matplotlib.pyplot as plt
import pandas as pd
import csv





allData = open("NE770All.csv", "a+")
dataFile = open(sys.argv[1], "r")


for line in dataFile:
	allData.write(line)

dataFile.close()
allData.close()

sys.exit(0)







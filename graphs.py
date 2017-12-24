import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import operator
import sys


#Since this module is run in a script, we pass in the name of the .csv file as a command-line argument
print ("Up to " + sys.argv[1])
data = pd.read_csv(sys.argv[1])



"""This creates a dictionary where each row (instant in time) maps to a dictionary of subbands and their associated dB values.
For now, we only consider the (time, subband) pairs for which the primary user is not present.
"""
 
channelsBelowThreshold = {}

for rowNumber, row in data.iterrows():
    colNumber = 0
    vulnerableChannels = {}
    for cell in row:
        if cell<(-90):
            vulnerableChannels[colNumber] = cell
        colNumber+=1
    channelsBelowThreshold[rowNumber] = vulnerableChannels


"""From the above dictionary, we create a parallel dictionary where the distance of each dB value to the threshold (-90) is stored.
""" 
allDistances = {}
rowNumber = 0
for row in channelsBelowThreshold:
    distances = {}
    dictionary = channelsBelowThreshold[row]
    colNumber = 0
    for col in dictionary:
        distances[col] = abs(dictionary[col]+90) # abs(dictionary[col] - (-90))
    allDistances[rowNumber] = distances
    rowNumber+=1

"""We create a new dictionary that finds which subbands are most vulnerable to a SSFD attack, by finding those channels who dB values differ
by at most 1 from the threshold. """
lessThan1Away = {}
rowNumber = 0
for row in allDistances:
    distances = {}
    dictionary = allDistances[row]
    for col in dictionary:
        if dictionary[col] <=1:
            distances[col] = dictionary[col]
    lessThan1Away[rowNumber] = distances
    rowNumber+=1

"""We manually compute a frequency table for the subbands, counting how many times each channel is vulnerable over the course of the 
time period of the .csv file.
"""
frequencies = {}
for row in lessThan1Away:
    dictionary = lessThan1Away[row]
    for col in dictionary:
        if col in frequencies:
            frequencies[col]+=1
        else:
            frequencies[col] = 1

"""We decompose this frequency table into two parallel vectors so that we can pass then to the plot functions
"""
channels = []
values = []
for channel in frequencies:
    channels.append(channel)
    values.append(frequencies[channel])


y_pos = np.arange(len(channels))
plt.bar(y_pos, values, align='center', alpha=0.5)
plt.xlabel("Channel #")
plt.xlim(1, 8200)
plt.ylabel("# of times channel is vulnerable")
plt.ylim(0, 1000)
plt.title("Most Vulnerable Channels in " + sys.argv[1])

"""Creates a unique name for each .csv to save them to the disk."""

index = sys.argv[1].find('.csv')
name = sys.argv[1][:index]
plt.savefig("Figures/" + name + ".png")

sys.exit(0)

#!C:\\Python36\\python
print("Content-Type: text/html")
print()

import plotly 
import numpy as np 
import cgi
import glob
import plotly.graph_objs as go

def drawHeatMap(allData, channelNo, subband): #This function draws the HeatMap using plotly
    dataPoints = []
    for i in range(3):
        dataPoints.append([]) # create 3 empty lists for storing 3 vulnerabilities for 7 days
    
    for matrix in allData:
        column = matrix[:, channelNo]
        distances = np.abs(-column-90)
        low = np.mean(distances <= 10, axis=0)
        mid = np.mean(distances <= 5, axis = 0)
        high = np.mean(distances<=1, axis=0)
        #print(low, mid, high)
        dataPoints[0].append(low)
        dataPoints[1].append(mid)
        dataPoints[2].append(high)
        #print(dataPoints)
        
    
    days = []
    for i in range(7):
        days.append("Day " + str(i+1))
    thresholds = ["low", "medium", "high"]
    heatMap = [go.Heatmap(z = dataPoints, x = days, y = thresholds)] #Draw the HeatMap
    
    plotly.offline.plot(heatMap, filename="heatMap" + subband+ "MHz" +str(channelNo)+".html")
	
	
def loadData(directory, extension): #loading all data for 7 days
    file_list = glob.glob(directory+"\\*" + extension)
    print(file_list)
    allData = []
    for file in file_list:
        data = np.load(file)["data"]
        allData.append(data)
    #print(allData)
    
    return allData
	
form = cgi.FieldStorage() 
#Getting field values from HTML files
channelNumber = int(form.getvalue("ChannelNumber"))
subband = form.getvalue("SubBand")

path = subband + "MHz"
extension = ".npz"
#Loading all data
allData = loadData(path, extension)
drawHeatMap(allData, channelNumber, subband)  
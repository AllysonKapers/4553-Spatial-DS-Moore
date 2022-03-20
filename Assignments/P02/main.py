import json
import csv
import geopandas
from statistics import mean
from numpy import sort
from shapely.geometry import box, Polygon, LineString, Point

#array to hold ufo data from csv
ufos = [] 


with open("/Users/AllyMoore/Documents/GitHub/4553-Spatial-DS/Resources/01_Data/cities.geojson") as f:
    cities = json.load(f)


with open("/Users/AllyMoore/Documents/GitHub/4553-Spatial-DS/Resources/01_Data/ufo_data.csv") as f:
    ufodata = csv.DictReader(f, delimiter = ',')

    #loads data from csv to ufos array
    for row in ufodata:
        ufos.append(row)

#creates array to hold all the points of ufo data
ufoPoints = []
for i in ufos:
   ufoPoints.append(Point(float(i['lon']), float(i['lat'])))

#creates array to hold the coordinates of the cities and 
#an array to hold to the names of the cities at matching indicies
#to improve readability when processing and storing data from geoseries
cityCoord = []
cityName =[]
for feature in cities["features"]:
    if feature['geometry']['point'] == 'Point':
        cityCoord.append(feature['geometry']['coordinates'])
        cityName.append()

#creates array to hold the cities
cities = []
for i in cityCoord:
    cities.append(Point(i))

#creates geo series of all cities coordinates and ufo points 
geoCity = geopandas.GeoSeries(cities)
geoUFO = geopandas.GeoSeries(ufoPoints)

#arrays to hold city and ufo distances to later write to json files
outputCities = []
outputUFO = []

#for loop to calculate and store the distances between each city "as the crow flies"
#also calculates the distance to each ufo sighting from each city to store and calculate 
#the average distance from the city to the 200 closest ufos
#smaller average distance = more ufos close to them 
for i in range(len(geoCity)):
    #array to hold tuples of the names and distances between each city
    distance = []

    #calculates the distance from every city in the series to geoCity[i]
    dis = geoCity.distance(geoCity[i])

    #creates an array of the distances stored in dis
    dis = dis.values

    #loads all the distances values into distance array as tuples of city names and distance
    for j in range(len(dis)):
        #excludes the value stored from the distance between geoCity[i] and itself in the geoseries
        if dis[i] != 0:
            distance.append((cityName[i],dis[i]))

    #creates dictionary for geoCity[i]
    city = {
        "city" : cityName[i],
        "distance" : distance
    }

    #adds city to the outputCity array to write to json 
    outputCities.append(city)
    
    
    #array to hold the distance to each UFO from geoCity[i]
    UFOdistance = []

    #calculates distance from geoCity[i] to each ufo sighting
    UFOdis = geoUFO.distance(geoCity[i])

    #stores distances values as an array
    UFOdis = UFOdis.values

    #sorts distances from smallest to largest
    UFOdis = sort(UFOdis)

    #creates a sub array for the closest 200 arrays to the city geoCity[i]
    UFO200 = UFOdis[0:200]

    #calculates the average distance from geoCity[i] to the 200 closets sighting
    avgUFOdis = mean(UFO200)

    cityUFO = {
        "city" : cityName[i],
        "average" : avgUFOdis
    }

    outputUFO.append(cityUFO)

#writes output arrays data to corresponding json files
with open("CityDistance.json", "w") as f:
    f.write(json.dumps(outputCities))

with open("UFOavg.json", "w") as f:
    f.write(json.dumps(outputCities))











## helper class for worldle project 
# runs the necessary functions to 
# calculate distance between two countries 
# to return to main program

from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2
from shapely.geometry import Polygon
import numpy as np
import geopandas as gps
import json
import os
import sys
from rich import print


## will need functions to:
#  [x]to open needed files 
#  [x]get the polygon of a given country
#  [x]find the distance between 2 countries
#  [x]handle a multipolygon to get the largest land mass of a country for calculations
#  [x]find selected country
#  [x]get center point 
#  [x]reduce the number of points in a polygon
#  [x] calculate bearing
#  []format output(separate class)
class SpatialMethods:
    #constructor: opens files needed
    def __init__(self):
        with open("continents.json") as f:
            self.__continents = json.load(f)
        with open("continents.geojson") as f:
            self.__countries = json.load(f)
        self.output = open("output.geojson", 'w')
    
    #finds largest polygon of a given country after passing a multipolygon
    def __single(self, mpoly):
        #tracks iterations to save max index
        i = 0
        index = i
        #saves the max permimeter of polygon
        max = 0

        #cycles through polygons in the mulipolygon to find max perimeter
        for poly in mpoly:
            if len(poly[0]) > max:
                index = i;
                max = len(poly[0])
            i += 1

        #returns the largest polygon 
        return mpoly[index][0]

    #finds the desired country from the json file  
    def __countDict(self, country):
        for continent in self.__continents:
            for countries in self.__continents[continent]:
                if countries['properties']["name"].lower() == country.lower():
                    return countries

    #consolodates country names
    def countryList(self):
        countList = []
        for continents in self.__continents:
            for countries in self.__continents[continents]:
                countList.append(countries['properties']['name'])
        return countList

    #returns the continent of a given country
    def getContinent(self, country):
        for continents in self.__continents:
            for countries in self.__continents:
                if country.lower() == countries['properties']['name'].lower():
                    return continents

    def displayPoly(self, country):
        country = self.__countDict(country)
        multipoly = country['geometry']['coordinates']
        

        return multipoly
        
    #gets polygon of a given country
    def getPolygon(self, country):
        count = self.__countDict(country)
        multipoly = count['geometry']['coordinates']
        poly = self.__single(multipoly)

        return poly

    #gets the center point of a polygon 
    def getCenter(self, poly):
        gseries = gps.GeoSeries(Polygon(poly))
        center = [gseries.centroid[0].x, gseries.centroid[0].y]
        return center

    #reduces polygon by a specific weight
    def reducePoints(self, country, weight):
        poly = self.getPolygon(country)
        series = gps.GeoSeries(Polygon(poly))
        poly = series.simplify(weight)[0]

        poly = np.asarray(poly.exterior.coords).tolist()

        return poly

    #calculate the distance between two points in miles
    def haversineDistance(self, lon1, lat1, lon2, lat2, units="miles"):
        
        radius = {"km": 6371, "miles": 3956}
        
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = radius[units]  # choose miles or km for results
        return c * r

    #uses distance equation to calculate the distance
    #between all perimeter points of the main country polygons
    #saves the points with the shortest distance to calculate the haversine distance
    #which will be the shortest distance between the countries from the points in the polygon
    #doesnt necessarily solve the problem of neighboring countries but the tests ran showed 
    #the distance of neighboring countries to be zero, but i didnt test all neighboring countries
    #*most accurate would be to use an algorithm to calculate the distance to a line 
    def distancePoints(self, poly1, poly2):
        #gets the largest polygon from the multippolygon
        series1 = gps.GeoSeries(gps.points_from_xy([x[0] for x in poly1], [y[1] for y in poly1]))
        series2 = gps.GeoSeries(gps.points_from_xy([x[0] for x in poly2], [y[1] for y in poly2]))
        
        min = -1
        for p1 in series1:
            for p2 in series2:
                distance = sqrt(((p1.x - p2.x)**2)+((p1.y-p2.y)**2))
                if min == -1:
                    min = distance
                    point1 = p1
                    point2 = p2
                elif min > distance:
                    min = distance
                    point1 = p1
                    point2 = p2

        lon1 = point1.x
        lat1 = point1.y
        lon2 = point2.x
        lat2 = point2.y
        #calculates the distance in miles and returns
        distMiles = self.haversineDistance(lon1, lat1, lon2, lat2)
        distMiles = round(distMiles, 3)
        return distMiles

    ##calculates the compass bearing for the line between two points
    def compass_bearing(self, pointA, pointB):
        if(type(pointA)!= tuple) or (type(pointB)!=tuple):
             raise TypeError("Only tuples are supported as arguments")
        
        lat1 = radians(pointA[0])
        lat2 = radians(pointB[0])

        diffLong = radians(pointB[1] - pointA[1])

        x = sin(diffLong) * cos(lat2)
        y = cos(lat1) * sin(lat2) - (sin(lat1) * cos(lat2) * cos(diffLong))

        initial_bearing = atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing


    


#test

## value returned is 8041.196 and the 
# capital to capital distance for closest estimate is 8185
if __name__ == "__main__":
    w = SpatialMethods()

    p1 = w.reducePoints('Afghanistan', .1)
    p2 = w.reducePoints('Aruba', .1)
    list = w.countryList()
    print(w.distancePoints(p1, p2))
    print(list[1])
    l = len(list)
    print(list[l-1])
    
#returns distance of zero
# if __name__ == "__main__":
#     w = SpatialMethods()
   


#     p1 = w.reducePoints('United States', .1)
#     p2 = w.reducePoints('Mexico', .1)

#     print(w.distancePoints(p1, p2))
#returns distance of 0
# if __name__ == "__main__":
#     w = SpatialMethods()

#     p1 = w.reducePoints('United States', .1)
#     p2 = w.reducePoints('Canada', .1)

#     print(w.distancePoints(p1, p2))
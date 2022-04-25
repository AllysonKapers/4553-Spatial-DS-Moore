## helper class for worldle project 
# runs the necessary functions to 
# calculate distance between two countries 
# to return to main program

from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2
from shapely.geometry import Polygon
import numpy as np
import geopandas as gps
import json


## will need functions to:
#  [x]to open needed files 
#  [x]get the polygon of a given country
#  []find the distance between 2 countries
#  []output data
#  [x]handle a multipolygon to get the largest land mass of a country for calculations
#  [x]find selected country
#  [x]get center point 
#  [x]reduce the number of points in a polygon
#  [] calculate bearing
class WorldleHelper:
    #constructor: opens files needed
    def __init__(self):
        with open("continents.json") as f:
            self.__globe = json.load(f)
        self.__output = open("output.geojson", 'w')
    
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
        for continent in self.__globe:
            for countries in self.__globe[continent]:
                if countries['properties']["name"].lower() == country.lower():
                    return countries



    #gets polygon of a given country
    def getPolygon(self, country):
        country = self.__countDict(country)
        multipoly = country['geometry']['coordinates']
        #gets the largest polygon from the multippolygon
        poly = self.__single(multipoly)

        return poly

    #gets the centerpoint of a polygon 
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

    def haversineDistance(self, point1, point2, units="miles"):
        
        radius = {"km": 6371, "miles": 3956}
        lon1 = point1.x
        lat1 = point1.y
        lon2 = point2.x
        lat2 = point2.y
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
        #calculates the distance in miles and returns
        distMiles = self.haversineDistance(point1, point2)
        distMiles = round(distMiles, 3)
        return distMiles


##test


## value returned is 8041.196 and the 
# capital to capital distance for closest estimate is 8185
if __name__ == "__main__":
    w = WorldleHelper()

    p1 = w.reducePoints('Afghanistan', .1)
    p2 = w.reducePoints('Aruba', .1)

    print(w.distancePoints(p1, p2))
#returns distance of zero
if __name__ == "__main__":
    w = WorldleHelper()

    p1 = w.reducePoints('United States', .1)
    p2 = w.reducePoints('Mexico', .1)

    print(w.distancePoints(p1, p2))
#returns distance of 0
if __name__ == "__main__":
    w = WorldleHelper()

    p1 = w.reducePoints('United States', .1)
    p2 = w.reducePoints('Canada', .1)

    print(w.distancePoints(p1, p2))
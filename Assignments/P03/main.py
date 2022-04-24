import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import pyproj
import json
import shapely
from shapely.geometry import box, Polygon, LineString, Point


from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from shapely.ops import unary_union, transform

#read files
citiesGDF = gpd.read_file("/Users/AllyMoore/Documents/GitHub/4553-Spatial-DS-Moore/Assignments/P03/cities_small.geojson")
ufoDF = pd.read_csv("/Users/AllyMoore/Documents/GitHub/4553-Spatial-DS-Moore/Assignments/P03/BetterUFOData.csv")
boundary = gpd.read_file("/Users/AllyMoore/Documents/GitHub/4553-Spatial-DS-Moore/Assignments/P03/us_border_shp/us_border.shp")


#geodataframe from pandas data frame

ufoGDF = gpd.GeoDataFrame(ufoDF, geometry=gpd.points_from_xy(ufoDF.lon, ufoDF.lat))


fig, ax = plt.subplots(figsize=(12, 10))
boundary.plot(ax=ax, color="gray")
citiesGDF.plot(ax=ax, markersize=2.5, color="blue")
ax.axis("off")
plt.axis('equal')


boundary = boundary.to_crs(epsg=3395)
gdf_proj = citiesGDF.to_crs(boundary.crs)
ufo_proj = ufoGDF.set_crs(boundary.crs)

boundary.crs


boundary_shape = unary_union(boundary.geometry)

coords = points_to_coords(gdf_proj.geometry)
ufoCoords = points_to_coords(ufo_proj.geometry)
region_polys, region_pts = voronoi_regions_from_coords(coords, boundary_shape)

fig, ax = subplot_for_map(figsize=(12, 10))
plot_voronoi_polys_with_points_in_area(ax, boundary_shape, region_polys, coords, region_pts)

#uncomment to see plot
#plt.show()

#holds the number of polygons in the voronoi diagram
i = len(region_polys)
#holds the length of region_polys for manipulation
end = i

#adds the point in the seventh 
#column of each row of data to the end of region_polys

for poi in list(ufoGDF.values):
    region_polys.update({end: poi[7]})
    end += 1

#creates a geoseries of all polygons and ufo points
all = gpd.GeoSeries(region_polys)

#holds output data to write to json
UFOpoly = []
#holds the polygon were on to ensure that there are 49 polygons and to
#output polygon name to json file
j = 0

#cycles through through the 'all' geoseries up until index i, which includes all the polygons
for pol in range(i):
    points = []
    #checks for polygon type
    if(type(all[pol]) == shapely.geometry.polygon.Polygon):
        points = np.asarray(all[pol].exterior.coords)
        points = points.tolist()

    else:
        for poly in all[pol]:
            coords = np.asarray(poly.exterior.coords)
            coords = coords.tolist()
            points.append(coords)
    
    #queries all ufo within a polygon
    query = all.sindex.query(all[i])
    ufos = []
    #adds points from the query to list of ufos
    for point in query:
        if type(all[point]) == shapely.geometry.point.Point:
            ufos.append([all[point].x, all[point].y])
    
    #keeps track of the name of the city associated with the polygon 
    name = citiesGDF.iloc[j,0]
    j = j+1

    #adds data to UFO poly gon to write to json 
    UFOpoly.append({
        'name' : name,
        'polygon' : points,
        'UFOs' : ufos
    })
#writes file
with open('PolysWithUFOs.json', 'w') as f:
    f.write(json.dumps(UFOpoly, indent=2))

import json
import geopandas as gpd

states = []
x = []
y = []
pop = []
#LIGHT TO DARK
colors = ['#F1F8E9','#DCEDC8','#C5E1A5', '#AED581', '#9CCC65','#8BC34A', '#7CB342', '#689F38', '#558B2F', '#33691E']



#opens map for state data
with open('states.geojson','r') as f:
    SData = gpd.read_file(f)

#opens json for all the city points
with open('cities.json' , 'r') as f:
    cities = json.load(f)

#formatting info to json for writing later
with open('states.geojson','r') as f:
    geoData = json.load(f)

    for feat in geoData['features']:
        #adds all state names to states
        states.append(feat['properties']['name'])
        
        feat['properties'].update({ "Population" : 0,
                                    "fill": "",
                                    "opacity": .8,
                                    "type": "state"
                                    })

#adds json data to respective lists
for city in cities:
    x.append(city['longitude'])
    y.append(city['latitude'])
    pop.append(city['population'])

#create geodataframe
cityDat = gpd.GeoDataFrame(pop, geometry = gpd.points_from_xy(x,y) )

#rtree
r = gpd.GeoSeries(SData['geometry'])
city = []

##Query points here
for i in range(cityDat[0].count()):
    try:
        #queries points within state
        que = r.sindex.query(cityDat['geometry'][i], predicate = 'within')[0]

        #increments state pop
        for feat in geoData['features']:
            #checks states match
            if states[que] == feat['properties']['name']:
                #adds population of city to cumulative total
                feat['properties']['Population'] += int(cityDat[0][i])
            city.append(states[que])
    except:
        print("Not in poly")
        city.append("Hawaii")

min = -1
max = -1
for feat in geoData['features']:
    if min == -1:
        min = feat['properties']['Population']
    if max == -1:
        max = feat['properties']['Population']
    if feat['properties']['Population'] < min:
        min = feat['properties']['Population']
    if feat['properties']['Population'] > max:
        max = feat['properties']['Population']

range = max - min
inc = range/10

#assigns color by population range
for feat in geoData['features']:
    if feat['properties']['Population'] == 0:
        feat['properties']['fill'] = "#FFFFFF"
    elif feat['properties']['Population'] <= inc:
        feat['properties']['fill'] = colors[0]
    elif feat['properties']['Population'] <= inc*2:
        feat['properties']['fill'] = colors[1]
    elif feat['properties']['Population'] <= inc*3:
        feat['properties']['fill'] = colors[2]
    elif feat['properties']['Population'] <= inc*4:
        feat['properties']['fill'] = colors[3]
    elif feat['properties']['Population'] <= inc*5:
        feat['properties']['fill'] = colors[4]
    elif feat['properties']['Population'] <= inc*6:
        feat['properties']['fill'] = colors[5]
    elif feat['properties']['Population'] <= inc*7:
        feat['properties']['fill'] = colors[6]
    elif feat['properties']['Population'] <= inc*8:
        feat['properties']['fill'] = colors[7]
    elif feat['properties']['Population'] <= inc*9:
        feat['properties']['fill'] = colors[8]
    elif feat['properties']['Population'] <= inc*10:
        feat['properties']['fill'] = colors[9]


#to create tiny polygons to represent cities
##first time using enumerate
##https://realpython.com/python-enumerate/
for j, cities in enumerate(cityDat['geometry']):
    x = cities.x
    y = cities.y
    #creates a small box for each city
    geometry = [[[cities.x + .15, cities.y + .15], [cities.x - .15, cities.y + .15], [cities.x - .15, cities.y - .15], [cities.x + .15, cities.y - .15], [cities.x + .15, cities.y + .15]]]


    #load each box into geoData to be displayed on map
    geoData['features'].append({
      "type": "Feature",
      "properties": {   "stroke": "#000000",
                        "stroke-width": 2,
                        "stroke-opacity": 1,
                        "fill": "",
                        "fill-opacity": 1,
                        'type': 'city',
                        'state': city[i]},
      "geometry": {
        "type": "Polygon",
        "coordinates": geometry
      }
    })


with open('out.geojson', 'w') as f:
    json.dump(geoData, f, indent=3)
    
        
        
    



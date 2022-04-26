import json
import geopandas as gpd

states = []
x = []
y = []
pop = []
#LIGHT TO DARK
colors = ['#E7E5F5','#D0CAEB','#B8B0E1', '#A096D6', '#887CCC','#7162C2', '#5947B8', '412DAE', '#2F2F6F', '#11115A']



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
                                    "opacity": 1,
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
#sorts by populations from smallest to largest
geoData['features'].sort(key = lambda x:x['properties']['Population'])
i = 0

#assigns color by population range
for feat in geoData['features']:
    if feat['properties']['Population'] == 0:
        feat['properties']['fill'] = "#FFFFFF"
    elif i < 5:
        feat['properties']['fill'] = colors[0]
    elif i < 10:
        feat['properties']['fill'] = colors[1]
    elif i < 15:
        feat['properties']['fill'] = colors[2]
    elif i < 20:
        feat['properties']['fill'] = colors[3]
    elif i < 25:
        feat['properties']['fill'] = colors[4]
    elif i < 30:
        feat['properties']['fill'] = colors[5]
    elif i < 35:
        feat['properties']['fill'] = colors[6]
    elif i < 40:
        feat['properties']['fill'] = colors[7]
    elif i < 45:
        feat['properties']['fill'] = colors[8]
    else:
        feat['properties']['fill'] = colors[9]
    i+=1


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
    
        
        
    



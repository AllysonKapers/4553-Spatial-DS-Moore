import json
import random

def randColor():
  r = lambda: random.randint(0,255)
  return ('#%02X%02X%02X' % (r(),r(),r()))


def makePoint(city, i):
  feature = {
    "type": "Feature",
    "properties": {
      "marker-color":randColor(),
      "marker-size" : "medium",
      "marker-symbol": i+1 
    },
    "geometry": {
      "type": "Point",
      "coordinates": [0,0]
    }
  }

  for key,val in city.items():
    if key == 'latitude':
      feature['geometry']['coordinates'][1] = val
    elif key == 'longitude':
      feature['geometry']['coordinates'][0] = val
    else:
      feature['properties'][key] = val

  return feature
  

# Change path as appropriate
with open("/Users/AllyMoore/Documents/GitHub/4553-Spatial-DS-Moore/Assignments/P01/cities_latlon_w_pop.json") as f:
  data = json.load(f)

#will hold an value for each state without duplicates
states = {}


#iterates through the entire json file
for item in data:
     
    #excludes Alaska and Hawaii because they aren't relevant to the assignment 
    if item['state'] != 'Alaska' and item['state'] != 'Hawaii':
        # adds first instance of each state in the json file to states
        if item['state'] not in states:
            states.update({
                item['state'] : {
                    "state" : item['state'],
                    "city" : item['city'],
                    "latitude" : item['latitude'],
                    "longitude" : item['longitude'],
                    "population" : item['population'] 
            }})
        ## checks current instance of a state against previous to ensure that 
        # the city within that statewith the highest population value is being stored in states 
        elif states[item['state']]['population'] < item['population']:
            states.update({
                item['state'] : {
                    "state" : item['state'],
                    "city" : item['city'],
                    "latitude" : item['latitude'],
                    "longitude" : item['longitude'],
                    "population" : item['population'] 
            }})

##list to store longitude values of the most populous cities per state
lng = []

##iterates through states to store each access and store each longitude value
for item in states:
    lng.append(states[item]['longitude'])

##sorts list of longitudes from west to east essentially
lng.sort()

##will store states sorted from west to east
points = []

##iterates through the sorted list of longitudes 
for spot in lng:
    ##iterates through the states to match each state to its longitude 
    # and adds each state to the points list based on longitude 
    for item in states:
        if states[item]['longitude'] == spot:
            points.append(states[item])

FeatureCollection = {
    "type" : "FeatureCollection",
    "features" : []
}
for i in range(len(points)):
    FeatureCollection["features"].append(makePoint(points[i], i))
    if i != len(points) -1:
        FeatureCollection['features'].append(
            {
                "type":"Feature",
                "properties":{
                    "lineColor": '#000000',
                    "LineWidth" : 3
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [points[i]['longitude'], points[i]['latitude']],
                        [points[i+1]['longitude'], points[i+1]['latitude']]
                    ]
                }
            }
        )

with open("Path.geojson","w") as f:
  f.write(json.dumps(FeatureCollection))
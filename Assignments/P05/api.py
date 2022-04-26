# Libraries for FastAPI
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# # Builtin libraries
# from math import radians, degrees, cos, sin, asin, sqrt, pow, atan2
# import os


# Classes from my module
from WorldleHelper import SpatialMethods

# from features import Feature
# from features import FeatureCollection 



"""
           _____ _____   _____ _   _ ______ ____
     /\   |  __ \_   _| |_   _| \ | |  ____/ __ \
    /  \  | |__) || |     | | |  \| | |__ | |  | |
   / /\ \ |  ___/ | |     | | | . ` |  __|| |  | |
  / ____ \| |    _| |_   _| |_| |\  | |   | |__| |
 /_/    \_\_|   |_____| |_____|_| \_|_|    \____/
The `description` is the information that gets displayed when the api is accessed from a browser and loads the base route.
Also the instance of `app` below description has info that gets displayed as well when the base route is accessed.
"""

description = """🚀
## Worldle Clone
### With Better Distance Calculations
"""

# Needed for CORS
origins = ["*"]


# This is the `app` instance which passes in a series of keyword arguments
# configuring this instance of the api. The URL's are obviously fake.
app = FastAPI(
    title="Worldle Clone",
    description=description,
    version="0.0.1",
    terms_of_service="http://killzonmbieswith.us/worldleterms/",
    contact={
        "name": "Worldle Clone",
        "url": "http://killzonmbieswith.us/worldle/contact/",
        "email": "chacha@killzonmbieswith.us",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
SpatialMethods = SpatialMethods()

# Needed for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






"""
  _____   ____  _    _ _______ ______  _____
 |  __ \ / __ \| |  | |__   __|  ____|/ ____|
 | |__) | |  | | |  | |  | |  | |__  | (___
 |  _  /| |  | | |  | |  | |  |  __|  \___ \
 | | \ \| |__| | |__| |  | |  | |____ ____) |
 |_|  \_\\____/ \____/   |_|  |______|_____/
 This is where your routes will be defined. Remember they are really just python functions
 that will talk to whatever class you write above. Fast Api simply takes your python results
 and packagres them so they can be sent back to your programs request.
"""

#done
@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")



#done
@app.get("/countries/")
async def getCountryNames():
    countries = SpatialMethods.countryList()
    return {'detail': 'Success','countries': countries} 


#done
@app.get("/country/{country_name}")
async def getCountry(country_name):
    """
    ### Description:
        Gets country polygon given a country name.
    ### Params:
        country_name (str)  : A country name to search for
    ### Returns:
        dict / json
    """
    # lowercase the country name then capitalize to fit the existing names.
    country_name = country_name.lower().title()

    # Go get the polygons
    polys = SpatialMethods.getPolygon(country_name)

    return {'detail': 'Success','polygon': polys}


#gets country center
@app.get("/getCenter/{country_name}")
async def countryCenter(country_name: str):
    country_name = SpatialMethods.getPolygon(country_name)
    CountryCenter = SpatialMethods.getCenter(country_name) # call the center point method
    return {'detail': 'Success','point': CountryCenter} # if successful, pass back the center point of the country
    

    

# #unused
# @app.get("/country_lookup/{key}")
# async def getCountryPartialMatch(key):
#     """
#     ### Description:
#         Get country names that partially match the key passed in.
#     ### Params:
#         key (str)  : a substring compared with the beginning of every country name.
#     ### Returns:
#         list / json
#     """
#     key = key.lower()
#     partial = []
#     names = SpatialMethods.countryList()
#     for name in names:
#         low_name = name.lower()
#         if low_name.startswith(key):
#             partial.append(name)
#     return partial



@app.get("/distance/{poly1}/{poly2}")
async def distance(poly1: str, poly2: str):
    

    poly1 = SpatialMethods.reducePoints(poly1, 0.25)
    poly2 = SpatialMethods.reducePoints(poly2, 0.25)
    
    distance = SpatialMethods.distancePoints(poly1,poly2)
    
    return {'detail':'Success','distance': distance}




@app.get("/cardinal/{poly1}/{poly2}")
async def cardinal(poly1:str, poly2: str):
    """
    This method works returns the cardinal direction given a bearing in decimal degrees.
    Params:
        degrees (float) : decimal degrees
    Returns:
        cardinal direction (string) : N, NNE ..... NW, NNW
    """
    dirs = [
        "N",
        "NE",
        "E",
        "SE",
        "S",
        "SW",
        "W",
        "NW",
    ]
    start = SpatialMethods.getPolygon(poly1)
    end = SpatialMethods.getPolygon(poly2)
    lon1, lat1 = SpatialMethods.getCenter(start)
    lon2, lat2 = SpatialMethods.getCenter(end)
    degrees = SpatialMethods.compass_bearing((lon1, lat1), (lon2, lat2))
    degrees = int(float(degrees))
    ix = int((degrees + 11.25) / 22.5)
    d = dirs[ix % 8]

    return {'detail': 'Success','direction': d}


"""
#This main block gets run when you invoke this file. How do you invoke this file?
#        python api.py 
#After it is running, copy paste this into a browser: http://127.0.0.1:8080 
#You should see your api's base route!
#Note:
#    Notice the first param below: api:app 
#    The left side (api) is the name of this file (api.py without the extension)
#    The right side (app) is the bearingiable name of the FastApi instance declared at the top of the file.
#"""
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)

from flask import Flask, redirect, render_template, request, session, jsonify
import requests
import pandas as pd
from shapely.geometry import Point
import pkg_resources
from geopandas import GeoDataFrame
#from pymongo import MongoClient

app = Flask(__name__)


#client = MongoClient()
#db = client.geojson_flask
#geodata_collection = db.geodata

@app.route('/')
def main():
    
    df = pd.DataFrame({#'zip':[19152,19047],
                   'Lat':[40.058841,40.202162],
                   'Lon':[-75.042164,-74.924594]})

    geometry = [Point(xy) for xy in zip(df.Lon, df.Lat)]



    gdf = GeoDataFrame(df, geometry=geometry)

    geoJSON = gdf.to_json()
    
    print(f"sending {geoJSON}")

    markers=[
   {
   'lat':40.058841,
   'lon':-75.042164,
   'popup':'This is the middle of the map.'
    }
   ]
    
    return render_template('main.html',markers=markers )#, geoJSON=[geoJSON])

if __name__ == "__main__":
    app.run(debug=True)

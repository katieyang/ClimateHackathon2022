from sys import prefix
import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import xarray as xa
import requests
import json
from hackathon_utils import get_zarr_from_blob

import os

# Connection string to blob storage has to be set if being run outside the Ocean Data Connector
os.environ['HACKATHON_CONNECTION_STR']='BlobEndpoint=https://stodpdaskuserspace.blob.core.windows.net/;SharedAccessSignature=sp=rl&st=2022-06-02T07:41:15Z&se=2022-06-10T15:41:15Z&spr=https&sv=2020-08-04&sr=c&sig=6dGq61DajRGtlIWqE8SMEEf1wbjXUjBgS5RxlcWqPoE%3D'    

# Opening the "Vessel CO2 Emissions and Traffic" dataset
store_list=get_zarr_from_blob('zarr/vessel_emissions_and_traffic')

def load_data():
    return xa.open_mfdataset(store_list, parallel=True, engine="zarr")

ds = load_data()

timeDF = ds.time.to_dataframe().drop_duplicates().reset_index(drop=True)
timeDF = timeDF.astype(str)

st.title("Shipping CO2 Emissions")

#fetching the region options from Marine Regions API
response = requests.get("https://www.marineregions.org/rest/getGazetteerRecordsByType.json/IHO%20Sea%20Area/?offset=0").json()

marine_regions = []
marine_regions_lon_lat = {} #(lon0,lat0,lon1,lat1)

for i in response:
    marine_regions.append(i["preferredGazetteerName"])
    marine_regions_lon_lat[i["preferredGazetteerName"]] = [i["minLongitude"],i["minLatitude"],i["maxLongitude"],i["maxLatitude"]]

marine_regions.sort()

region = st.sidebar.selectbox(
     'Which region are you interested in?',
     marine_regions)

lon0,lat0,lon1,lat1=marine_regions_lon_lat[region][0],marine_regions_lon_lat[region][1],marine_regions_lon_lat[region][2],marine_regions_lon_lat[region][3]

#lon0,lat0,lon1,lat1=-13.33779952,50.22380672,9.75926460,63.38491144 # bounding box

vessel_type = st.sidebar.selectbox(
     'Which vessel types are you interested in?',
     ('Cargo', 'Fishing', 'Passenger','Tanker','Total'))

co2 = ""

if vessel_type == 'Cargo':
    co2 = "co2_cargo"
elif vessel_type == 'Fishing':
    co2 = "co2_fishing"
elif vessel_type == 'Passenger':
    co2 = "co2_passenger"
elif vessel_type == 'Tanker':
    co2 = "co2_tanker"
else:
    co2 = "co2_total"

start_date, end_date = st.sidebar.select_slider("What time period are you interested in?",options=timeDF,value=["2020-01-01","2021-01-01"])

st.sidebar.checkbox("Green Corridor (Check to show - NOTE: NOT IMPLEMENTED)")
st.sidebar.checkbox("Blue Corridor (Check to show - NOTE: NOT IMPLEMENTED)")

mapDF = ds.sel(lon=slice(lon0,lon1), lat=slice(lat0,lat1), time=slice(start_date,end_date))[co2].compute().to_dataframe()

mapDF.reset_index(inplace=True)

mapDF = mapDF.groupby(['lat','lon']).sum()

mapDF.reset_index(inplace=True)

mapDF = mapDF[(mapDF[co2]>0)]   #drop everything where there's no emissions

mapDF = mapDF[['lon','lat',co2]].iloc[::5, :]   #take every 5th row because my computer isn't powerful enough to handle more...

#add a column indicating opacity on scale of 0 to 255
mapDF['opacity'] = round(mapDF[co2]/max(mapDF[co2])*255).astype(int)

#count = (mapDF['co2_total'] == 0).sum()
#st.write('Count of zeros in Column  co2_total : ', count)

#calculate total emissions in mT
total_emissions = round(sum(mapDF[co2])/1000000)

st.write("CO2 emissions from ", vessel_type.lower(), " vessels in the ", region, " from ", start_date, " to ", end_date, " is estimated to be ", total_emissions, " mT. This is equal to emissions from ", round(total_emissions*0.65), "Canadian households' electrictiy use over one year.")

#st.write(mapDF)

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=(lat0+lat1)/2,
         longitude=(lon0+lon1)/2,
         zoom=7,
         pitch=50,
     ),
     layers=[
        pdk.Layer(
        "ColumnLayer",
        data=mapDF,
        get_position=["lon", "lat"],
        get_elevation=co2,
        elevation_scale=0.000001,
        radius=5000,
        get_fill_color= ["opacity",0,0,"opacity"],
        pickable=False,
        auto_highlight=False,
    )
     ],
 ))

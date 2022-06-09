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

st.title("The Challenge")
st.write("Hub Ocean and Cognite (Norway) challenged Climate Hackathon 2022 teams to develop a solution that makes it easier to gain insight into ship traffic and CO2 emissions, so that individuals and institutions can take effective action to protect our ocean and planets.")

st.title("The Solution")
st.write("This app helps users explore, visualize, and learn more about CO2 emissions from different types of vessels in different parts of the world over time. It helps contextualize the amount of CO2 emissions and will hopefully serve as a powerful call to action.")

st.write("\nTechnologies used in the solution include:")
st.image(["https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png","https://devblogs.microsoft.com/visualstudio/wp-content/uploads/sites/4/2020/04/devblog-brand-visualstudiowin2019.png","https://cdn.analyticsvidhya.com/wp-content/uploads/2021/06/39595st.jpeg","https://s3.amazonaws.com/challengepost/sponsors/logos/000/025/994/highres/hubocean-logo_%281%29.png","https://www.vliz.be/images/news/MarineRegions-banner.jpg","https://www.itprotoday.com/sites/itprotoday.com/files/styles/article_featured_retina/public/AzureCloud_1_5.jpg?itok=htcIZVHD"], width=150)

st.title("The Vision")
st.write("Additional features that were planned but not implemented due to lack of time include: 1) a geolocation feature so that the first visualization generated is based on the sea area closest to the user's IP address, 2) a box where users can input an email to their local political representative encouraging them to take action on protecting the ocean, and 3) a way to view green and blue corridors on the visualization and visualize the impact they would have.")

st.title("Team")
st.write("Solo hacker passionate about the climate from Ontario, Canada. [Feel free to add me on LinkedIn :)](https://www.linkedin.com/in/katie-yang/)")
st.image("https://i.ibb.co/PWd8Y4b/Capture.png", caption='Katie Yang')
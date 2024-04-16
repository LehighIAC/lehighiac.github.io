import folium as fl
from streamlit_folium import st_folium
import streamlit as st
from datetime import time, timedelta

def get_pos(lat, lng):
  return lat, lng

# Loads map to show bethlehem, PA
m = fl.Map(location=[40.62, -75.37], zoom_start=13)
# Adds a popup returning the latitude and longitude of the clicked location
m.add_child(fl.LatLngPopup())
# Variable to store last clicked location
data = None
# Determine column layout
# mapContainer = st.container(border=True)
mapCol = st.container()
hoursCol,dataCol = st.columns([0.8, 0.2], gap="medium")

# Adds the map to streamlit
with mapCol:
  map = st_folium(m, width=800, height=500)

with dataCol:  
  mode = st.radio("Select mode", ("Cooling", "Heating"))
  method = st.radio("Select method", ("Deg. Hours", "Deg. Days"))
  tempUnit = st.radio("Select Temp Unit", ("Celsius", "Fahrenheit"))
  # Handle temperature input and conversions
  if tempUnit == "Celsius":
    baseTemp = st.number_input("Enter Base Temp", 0, 100, 18)
    setbackTemp = st.number_input("Enter Historical Temp", 0, 100, 18)
  else:
    baseTemp = st.number_input("Enter Base Temp", 32, 212, 65)
    setbackTemp = st.number_input("Enter Historical Temp", 32, 212, 65)
  calculate = st.button("Calculate")

with hoursCol:
  mondayHours = st.slider("Monday Hours:", value=(time(9), time(17)), step=timedelta(minutes=30))
  tuesdayHours = st.slider("Tuesday Hours:", value=(time(9), time(17)), step=timedelta(minutes=30))
  wednesdayHours = st.slider("Wednesday Hours:", value=(time(9), time(17)), step=timedelta(minutes=30))
  thursdayHours = st.slider("Thursday Hours:", value=(time(9), time(17)), step=timedelta(minutes=30))
  fridayHours = st.slider("Friday Hours:", value=(time(9), time(17)), step=timedelta(minutes=30))
  saturdayHours = st.slider("Saturday Hours:", value=(time(9), time(17)), step=timedelta(minutes=30))
  sundayHours = st.slider("Sunday Hours:", value=(time(9), time(17)), step=timedelta(minutes=30))

mholiday = st.checkbox("Holiday")
# Retrieves the last clicked location
if map.get('last_clicked'):
  data = get_pos(map['last_clicked']['lat'], map['last_clicked']['lng'])

def calculate():
  # Select mode
  sign = 1 if mode == "Cooling" else -1

  if sign == 1 and baseTemp > setbackTemp:
    st.write("Setback temperature must be higher than base temperature")
  if sign ==-1 and baseTemp < setbackTemp:
    st.write("Setback temperature must be lower than base temperature")
    



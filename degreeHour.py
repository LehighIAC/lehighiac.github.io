import folium as fl
from streamlit_folium import st_folium
import streamlit as st
from datetime import time, timedelta, datetime
from meteostat import Point, Daily, Hourly, units
from geopy.geocoders import Nominatim

def get_pos(lat, lng):
  return lat, lng

def calculation(mapData, mode, method, tempUnit, baseTemp, setbackTemp, history):
  try:
    sign = 1 if mode == "Cooling" else -1

    if sign == 1 and baseTemp > setbackTemp:
      raise Exception("Setback temperature must be higher than base temperature")
    if sign == -1 and baseTemp < setbackTemp:
      raise Exception("Setback temperature must be lower than base temperature")
    # Set time range
    starttime = datetime(2023 - history, 1, 1)
    endtime = datetime(2022, 12, 31, 23, 59)
    # Fetch Data
    Point.method = 'nearest'
    # Radius for nearby stations in meters  
    Point.radius = 50000
    plant = Point(mapData[0], mapData[1])

    if method == "Deg. Hours":
      data = Hourly(plant, starttime, endtime)
      if tempUnit == "Fahrenheit":
        data = data.convert(units.imperial)
      data.normalize()
      data = data.interpolate()
      data = data.fetch()
      # Calculate degree hours
      data['basetemp'] = baseTemp
      data['day'] = data.index.dayofweek
      data['hour'] = data.index.hour
      for day in range(7):
        data.loc[(data['day'] == day) & (data['hour'] < schedule[day][0]), 'basetemp'] = setbackTemp
        data.loc[(data['day'] == day) & (data['hour'] >= schedule[day][1]), 'basetemp'] = setbackTemp
      data['degreehour'] = data.apply(lambda x: max((x['temp'] - x['basetemp']) * sign, 0), axis=1)
      result = data.degreehour.sum()/history
    else:
      data = Daily(plant, starttime, endtime)
      if tempUnit == "Fahrenheit":
        data = data.convert(units.imperial)
      data.normalize()
      data = data.interpolate()
      data = data.fetch()
      # Calculate degree days
      data['degreeday'] = data.apply(lambda x: max((x['tavg'] - baseTemp) * sign, 0), axis=1)
      result = data.degreeday.sum()/history
    return result
  except Exception as e:
    st.warning(e)

# Default Bethlehem, PA location coordinates
lat = 40.62
lon = -75.37
# Check if address is valid
address = st.sidebar.text_input("Enter Address", key="address", placeholder="City, State")
geolocator = Nominatim(user_agent="degreeHour app")
location = geolocator.geocode(address)
if location is not None:
  lat = location.latitude
  lon = location.longitude
# Loads map to show bethlehem, PA
m = fl.Map(location=[lat, lon], zoom_start=13)
# Adds a popup returning the latitude and longitude of the clicked location
m.add_child(fl.LatLngPopup())
# Variable to store last clicked location
mapData = None
# Determine column layout
mapCol = st.container()
programInfo = st.container()
holidayCol, dayCol, hoursCol, dataCol = st.columns([0.1, 0.1, 0.56, 0.2], gap="small")

# Days of the week list
dayOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Adds the map to streamlit
with mapCol:
  st.title("IAC Degree Days/Hour Calculator", anchor="top")
  map = st_folium(m, width=800, height=500)
with programInfo:
  st.subheader("Thermostat Programming Schedule", divider="red")
  with holidayCol:
    st.text("Holiday")
    holiday = []
    for day in range(7):
      holiday.append(st.checkbox(f"{dayOfWeek[day]}", label_visibility="hidden", key=day))
    
  with dayCol:
    st.text("All Day")
    allDay = []
    for day in range(7):
      allDay.append(st.checkbox(f"{dayOfWeek[day]}", label_visibility="hidden"))

  with hoursCol:
    hourly = []
    for day in range(7):
      if holiday[day]:
        hourly.append(st.slider(f"{dayOfWeek[day]} Hours:", value=(time(0), time(0))))
      elif allDay[day]:
        hourly.append(st.slider(f"{dayOfWeek[day]} Hours:", value=(time(0), time(23, 59))))
      else:
        hourly.append(st.slider(f"{dayOfWeek[day]} Hours:", value=(time(9), time(17)), step=timedelta(minutes=30)))

  # Retrieves the last clicked location
  if map.get('last_clicked'):
    mapData = get_pos(map['last_clicked']['lat'], map['last_clicked']['lng'])
  # Storing schedule
  schedule = []
  for day in range(7):
    # Checks for minute intervals
    start = int(time.strftime(hourly[day][0], "%H")) + (float(time.strftime(hourly[day][0], "%M"))/60)
    end = int(time.strftime(hourly[day][1], "%H")) + (float(time.strftime(hourly[day][1], "%M"))/60)
    schedule.append((start, end))

  with dataCol:  
    mode = st.radio("Select mode", ("Cooling", "Heating"))
    method = st.radio("Select method", ("Deg. Hours", "Deg. Days"))
    tempUnit = st.radio("Select Temp Unit", ("Celsius", "Fahrenheit"))
    # Handle temperature input
    if tempUnit == "Celsius":
      baseTemp = st.number_input("Enter Base Temp", 0, 100, 18)
      setbackTemp = st.number_input("Enter Setback Temp", 0, 100, 18)
    else:
      baseTemp = st.number_input("Enter Base Temp", 32, 212, 65)
      setbackTemp = st.number_input("Enter Setback Temp", 32, 212, 65)
    history = st.number_input("History (Years)", 1, 5, 1)
    calculate = st.button("Calculate")

    if calculate:
      result = calculation(mapData, mode, method, tempUnit, baseTemp, setbackTemp, history)
      if result is not None:
        st.write(f"Average {mode} {method}: {int(result)}")
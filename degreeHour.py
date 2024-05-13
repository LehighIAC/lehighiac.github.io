import folium as fl
from streamlit_folium import st_folium
import streamlit as st
from datetime import time, timedelta, datetime
from meteostat import Point, Daily, Hourly

def get_pos(lat, lng):
  return lat, lng

# Loads map to show bethlehem, PA
m = fl.Map(location=[40.62, -75.37], zoom_start=13)
# Adds a popup returning the latitude and longitude of the clicked location
m.add_child(fl.LatLngPopup())
# Variable to store last clicked location
mapData = None
# Determine column layout
mapCol = st.container()
programInfo = st.container()
holidayCol, dayCol, hoursCol, dataCol = st.columns([0.1 ,0.1, 0.6, 0.2], gap="small")

# Adds the map to streamlit
with mapCol:
  st.title("IAC Degree Days/Hour Calculator", anchor="top")
  map = st_folium(m, width=800, height=500)
with programInfo:
  st.subheader("Thermostat Programming Schedule", divider="red")

  with holidayCol:
    st.text("Holiday")
    # Text label hidden and written weird for spacing
    monHoliday = st.checkbox("MonOff", label_visibility="hidden")
    tuesHoliday = st.checkbox("TueOff", label_visibility="hidden")
    wenHoliday = st.checkbox("WensdOff", label_visibility="hidden")
    thursHoliday = st.checkbox("ThurOff", label_visibility="hidden")
    friHoliday = st.checkbox("FridOff", label_visibility="hidden")
    SatHoliday = st.checkbox("SatdyOff", label_visibility="hidden")
    sunHoliday = st.checkbox("SunOff", label_visibility="hidden")
    
  with dayCol:
    st.text("All Day")
    # Text label hidden and written weird for spacing
    monAllDay = st.checkbox("MallDay", label_visibility="hidden")
    tuesAllDay = st.checkbox("TallDay", label_visibility="hidden")
    wenAllDay = st.checkbox("WENallDay", label_visibility="hidden")
    thursAllDay = st.checkbox("THallDy", label_visibility="hidden")
    friAllDay = st.checkbox("FallDay", label_visibility="hidden")
    satAllDay = st.checkbox("STallDay", label_visibility="hidden")
    sunAllDay = st.checkbox("SallDay", label_visibility="hidden")

  with hoursCol:
    if monHoliday:
      t1, t2 = 0, 0
    elif monAllDay:
      t1, t2 = 0, 23
    else:
      t1, t2 = 9, 17
    monHours = st.slider("Monday Hours:", value=(time(t1), time(t2)), step=timedelta(hours=1))
    
    if tuesHoliday:
      tuesHours = st.slider("Tuesday Hours:", value=(time(0)))
      tuesHours = [0, 0]
    elif tuesAllDay:
      tuesHours = st.slider("Tuesday Hours:", value=(time(0), time(23, 59)))
      tuesHours = [0, 24]
    else:
      tuesHours = st.slider("Tuesday Hours:", value=(time(9), time(17)), step=timedelta(hours=1))
    
    if wenHoliday:
      wedHours = st.slider("Wednesday Hours:", value=(time(0)))
      wedHours
    elif wenAllDay:
      wedHours = st.slider("Wednesday Hours:", value=(time(0), time(23, 59)))
      wedHours = [0, 24]
    else:
      wedHours = st.slider("Wednesday Hours:", value=(time(9), time(17)), step=timedelta(hours=1))
    
    if thursHoliday:
      thursHours = st.slider("Thursday Hours:", value=(time(0)))
      thursHours = [0, 0]
    elif thursAllDay:
      thursHours = st.slider("Thursday Hours:", value=(time(0), time(23, 59)))
      thursHours = [0, 24]
    else:
      thursHours = st.slider("Thursday Hours:", value=(time(9), time(17)), step=timedelta(hours=1))
  
    if friHoliday:
      friHours = st.slider("Friday Hours:", value=(time(0)))
      friHours = [0, 0]
    elif friAllDay:
      friHours = st.slider("Friday Hours:", value=(time(0), time(23, 59)))
      friHours = [0, 24]
    else:   
      friHours = st.slider("Friday Hours:", value=(time(9), time(17)), step=timedelta(hours=1))
    
    if SatHoliday:
      satHours = st.slider("Saturday Hours:", value=(time(0)))
    elif satAllDay:
      satHours = st.slider("Saturday Hours:", value=(time(0), time(23, 59)))
    else:
      satHours = st.slider("Saturday Hours:", value=(time(9), time(17)), step=timedelta(hours=1))
    
    if sunHoliday:
      sunHours = st.slider("Sunday Hours:", value=(time(0)))
    elif sunAllDay:
      sunHours = st.slider("Sunday Hours:", value=(time(0), time(23, 59)))
    else:
      sunHours = st.slider("Sunday Hours:", value=(time(9), time(17)), step=timedelta(hours=1))

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
    history = st.number_input("History (Years)", 1, 10, 1)
    calculate = st.button("Calculate")

# Retrieves the last clicked location
if map.get('last_clicked'):
  mapData = get_pos(map['last_clicked']['lat'], map['last_clicked']['lng'])

schedule = []
schedule.append((int(time.strftime(monHours[0], "%H")), int(time.strftime(monHours[1], "%H"))))
schedule.append((int(time.strftime(tuesHours[0], "%H")), int(time.strftime(tuesHours[1], "%H"))))
schedule.append((int(time.strftime(wedHours[0], "%H")), int(time.strftime(wedHours[1], "%H"))))
schedule.append((int(time.strftime(thursHours[0], "%H")), int(time.strftime(thursHours[1], "%H"))))
schedule.append((int(time.strftime(friHours[0], "%H")), int(time.strftime(friHours[1], "%H"))))
schedule.append((int(time.strftime(satHours[0], "%H")), int(time.strftime(satHours[1], "%H"))))
schedule.append((int(time.strftime(sunHours[0], "%H")), int(time.strftime(sunHours[1], "%H"))))

sign = 1 if mode == "Cooling" else -1
if sign == 1 and baseTemp > setbackTemp:
  st.write("Setback temperature must be higher than base temperature")
if sign ==-1 and baseTemp < setbackTemp:
  st.write("Setback temperature must be lower than base temperature")
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
  data.normalize()
  data = data.interpolate()
  data = data.fetch()
  # Calculate degree days
  data['degreeday'] = data.apply(lambda x: max((x['tavg'] - baseTemp) * sign, 0), axis=1)
  result = data.degreeday.sum()/history

st.write(f"Result: {result}")

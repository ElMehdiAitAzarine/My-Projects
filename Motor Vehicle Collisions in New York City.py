import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
DATA_URL = (
"C:/Users/hp/Desktop/Motor_Vehicle_Collisions_-_Crashes.csv"
)
st.title("Motor Vehicle Collisions in New York City")
st.markdown("this application is a Streamlit dashbord that can be used"
"to analyze motor vehicle collisions in NYC 🏍️")
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL,nrows=nrows,parse_dates=[['CRASH DATE','CRASH TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns',inplace=True)
    data.rename(columns={'crash_date''crash_time' : 'date/time'},inplace=True)
    data.drop(data.loc[data['latitude']==int(0.0000)].index, inplace=True)
    return data

data = load_data(100000)
data.rename(columns={'number of persons injured' : 'nopi'},inplace=True)
st.header("Where are the most peaple injured in NYC?")
injured_peaple = st.slider("Number of Persons Injured In Vehicule Collision",0,20)
st.map(data.query('nopi >= @injured_peaple')[["latitude","longitude"]].dropna(how="any"))
data.rename(columns={'nopi' : 'number of persons injured'},inplace=True)

st.header('How Many Collision Occur During a Given Time Of Day ?')
hour = st.slider("Hour to look at",0,23)
data = data[data['crash date_crash time'].dt.hour == hour]

st.markdown("Vehicule Collisions between %i:00 and %i:00" % (hour, (hour+1)%24))
midpoint = (np.average(data['latitude']),np.average(data['longitude']))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
          "latitude": midpoint[0],
          "longitude": midpoint[1],
          "zoom" : 11,
          "pitch":50,

        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data = data[['crash date_crash time','latitude','longitude']],
                get_position=['longitude','latitude'],
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0,1000],
        ),
            ],
    ))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour + 1) %24)
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data[date/time].dt.hour<(hour +1))
    ]
hist = np.histogram(filtered['date/time'].dt.minute,bins=60)
chart_data = pd.DataFrame({'minute':range(60), 'crashes':hist})
fig = pd.bar(chart_data, x='minute', y='crashes', hover_data=['minute','crashes'], height=400)
st.write(fig)

if st.checkbox("Show Raw Data",True):
  st.subheader('Raw Data')
  st.write(data)

 

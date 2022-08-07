import streamlit as st
import pandas as pd
import numpy as np

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
    data.rename(columns={'crash_date_crash_time' : 'date/time'},inplace=True)
    data.drop(data.loc[data['latitude']==int(0.0000)].index, inplace=True)
    return data

data = load_data(100000)
data.rename(columns={'number of persons injured' : 'nopi'},inplace=True)
st.header("Where are the most peaple injured in NYC?")
injured_peaple = st.slider("Number of Persons Injured In Vehicule Collision",0,20)
st.map(data.query('nopi >= @injured_peaple')[["latitude","longitude"]].dropna(how="any"))
data.rename(columns={'nopi' : 'number of persons injured'},inplace=True)

st.header('How Many Collision Occur During A Given Time Of Day ?')
hour = st.selectbox("Hour to look at", range(0,24),1)
data = data[data['crash date_crash time'].dt.hour == hour]





if st.checkbox("Show Raw Data",True):
  st.subheader('Raw Data')
  st.write(data)


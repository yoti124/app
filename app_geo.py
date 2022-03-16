import time
import base64
import streamlit as st
import pandas as pd
# import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import plotly.express as px
import folium
import chardet
from folium.plugins import MarkerCluster

st.title("Geocoding Application in Python")
st.markdown("Uppload a xlsx File with address columns (Street name & number & City)")

def convert_address_to_geocode(df):
    geolocator = Nominatim(user_agent="sample app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    df["Address"] = df["Address"].astype(str)
    df["loc"] = df["Address"].apply(geocode)
    df["point"]= df["loc"].apply(lambda loc: tuple(loc.point) if loc else None)
    df[['lat', 'lon', 'altitude']] = pd.DataFrame(df['point'].to_list(), index=df.index)
    return df

# @st.cache(persist=True, suppress_st_warning=True)
def display_map(df):
    m = folium.Map(location=df[["lat", "lon"]].mean().to_list(), zoom_start=8)

# if the points are too close to each other, cluster them, create a cluster overlay with MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)

# draw the markers and assign popup and hover texts
# add the markers the the cluster layers so that they are automatically clustered
    for i,r in df.iterrows():
        location = (r["lat"], r["lon"])
        folium.Marker(location=location,popup = r['loc'],tooltip=r['loc']).add_to(marker_cluster) 
    return m

def download_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}">Download csv File</a> (right-click and save as &lt;some_name&gt;.csv)'
    return href

def main():
    file = st.file_uploader("Choose a file")
    if file is not None:
        file.seek(0)
        result = chardet.detect(rawdata.read(100))["encoding"]
        df = pd.read_csv(file,encoding=result)
        with st.spinner('Reading csv File...'):
            time.sleep(5)
            st.success('Done!')
        st.write(df.head())
        st.write(df.shape)



        # cols = df.columns.tolist()

        st.subheader("Choose Address Columns from the Sidebar")
        st.info("Example correct address: אגריפס 1 ירושלים")
    
    if st.checkbox("Address Formatted correctly (Example Above)"):
        df_address = convert_address_to_geocode(df)
        # st.write(df_address)
        with st.spinner('Geocoding Hold tight...'):
            # time.sleep(5)
            st.success('Done!')
            # st.write(df_address)
            # display_map(df_address)
            st.markdown(download_csv(df_address), unsafe_allow_html=True)


if __name__ == "__main__":
    main()

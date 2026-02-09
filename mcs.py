import streamlit as st

# Configuration
GOOGLE_MAPS_API_KEY = "AIzaSyCeZu24qMrH7VwVkj3aHmiioGRwO4cgAHw"
MCS_LAT = 33.6449
MCS_LNG = 72.9919

st.set_page_config(page_title="MCS Street View", layout="wide")
st.title("🎓 MCS Street View Explorer")

# Input latitude and longitude (optional)
col1, col2 = st.columns(2)
with col1:
    lat = st.number_input("Latitude", value=MCS_LAT, format="%.6f")
with col2:
    lng = st.number_input("Longitude", value=MCS_LNG, format="%.6f")

# Create Street View URL
street_view_url = (
    f"https://maps.googleapis.com/maps/api/streetview"
    f"?size=800x600&location={lat},{lng}&heading=210&pitch=10&fov=90&key={GOOGLE_MAPS_API_KEY}"
)

st.image(street_view_url, caption="MCS Street View", use_column_width=True)
locations = {
    "Main Gate": (33.6427, 72.9924),
    "Admin Block": (33.6429, 72.9919),
    "CS Block": (33.6432, 72.9925),
    "Library": (33.6425, 72.9929),
    "Hostel": (33.6439, 72.9931)
}

choice = st.selectbox("Select Location", list(locations.keys()))
lat, lng = locations[choice]

street_view_url = (
    f"https://maps.googleapis.com/maps/api/streetview"
    f"?size=800x600&location={lat},{lng}&heading=210&pitch=10&fov=90&key={GOOGLE_MAPS_API_KEY}"
)

st.image(street_view_url, caption=f"{choice} Street View", use_column_width=True)

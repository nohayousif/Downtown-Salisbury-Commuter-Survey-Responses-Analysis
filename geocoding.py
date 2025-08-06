import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# import data
df = pd.read_csv('data/Downtown Salisbury Commuter Survey (Responses).csv')

# initiate geolocator
geolocator = Nominatim(user_agent="nohagyousif@gmail.com")

def geocode(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            print(f"geocoded: {address} -> ({location.latitude}, {location.longitude})")
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([np.nan, np.nan])
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"geocoding error: {e}")
        return pd.Series([np.nan, np.nan])

# geocode business addresses for mapping
df[['Work Latitude', 'Work Longitude']] = df["Where do you work (business address)?"].apply(geocode)

# geocode home addresses for mapping
df[['Home Latitude', 'Home Longitude']] = df["Where do you live (neighborhood and/or address)?"].apply(geocode)
df.to_csv('data/Downtown Salisbury Commuter Survey (Responses) with Geocoding', index=False)

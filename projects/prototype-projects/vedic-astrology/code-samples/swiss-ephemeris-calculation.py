"""
Swiss Ephemeris Integration for Vedic Astrology
Demonstrates high-precision planetary calculations.
"""

import swisseph as swe
from datetime import datetime
import pytz
from collections import OrderedDict

# Define constants
PLANETS = OrderedDict([
    (swe.SUN, "Sun"),
    (swe.MOON, "Moon"),
    (swe.MARS, "Mars"),
    (swe.MERCURY, "Mercury"),
    (swe.JUPITER, "Jupiter"),
    (swe.VENUS, "Venus"),
    (swe.SATURN, "Saturn"),
    (swe.MEAN_NODE, "Rahu"),  # North Node
    (swe.MEAN_APOG, "Ketu")   # South Node
])

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def calculate_planet_positions(date, time, lat, lon, timezone):
    """Calculate planetary positions for given date and location"""
    # Convert to UTC
    tz = pytz.timezone(timezone)
    dt = tz.localize(datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M"))
    utc_dt = dt.astimezone(pytz.UTC)
    
    # Convert to Julian Day
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day,
                    utc_dt.hour + utc_dt.minute/60.0)
    
    # Calculate Ayanamsa (Lahiri for Vedic astrology)
    ayanamsa = float(swe.get_ayanamsa(jd))
    
    # Calculate positions
    positions = {}
    for planet_id, planet_name in PLANETS.items():
        try:
            # Get planet position
            result = swe.calc_ut(jd, planet_id)
            
            # Extract longitude from result
            if isinstance(result, tuple) and len(result) == 2:
                if isinstance(result[0], tuple):
                    longitude = result[0][0]
                else:
                    longitude = result[0]
            else:
                raise ValueError(f"Unexpected result format: {result}")
            
            # Convert to sidereal (Vedic) longitude
            sidereal_longitude = (float(longitude) - ayanamsa) % 360
            sign_index = int(sidereal_longitude / 30)
            degree_in_sign = sidereal_longitude % 30
            
            positions[planet_name] = {
                'longitude': sidereal_longitude,
                'sign': ZODIAC_SIGNS[sign_index],
                'degree_in_sign': round(degree_in_sign, 2),
                'house': calculate_house(sidereal_longitude, lat, lon, jd)
            }
        except Exception as e:
            print(f"Error calculating {planet_name}: {e}")
            positions[planet_name] = None
    
    return positions

def calculate_house(longitude, lat, lon, jd):
    """Calculate house placement using Equal House system"""
    # Calculate Ascendant
    ascendant = swe.houses(jd, lat, lon, b'P')[1][0]  # Ascendant longitude
    
    # Apply ayanamsa for sidereal
    ayanamsa = float(swe.get_ayanamsa(jd))
    sidereal_asc = (ascendant - ayanamsa) % 360
    
    # Calculate house (Equal House system)
    house_diff = (longitude - sidereal_asc) % 360
    house = int(house_diff / 30) + 1
    
    return house

def get_ayanamsa(jd):
    """Get Lahiri Ayanamsa for Vedic calculations"""
    return float(swe.get_ayanamsa(jd))

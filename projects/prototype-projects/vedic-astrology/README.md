# Vedic Astrology Birth Chart Calculator

A Flask web application that calculates and displays Vedic (sidereal) birth charts and planetary positions based on birth date, time, and location using high-precision Swiss Ephemeris calculations.

## Overview

The Vedic Astrology Calculator is a specialized application that computes accurate planetary positions and generates interactive birth chart visualizations. It uses the Swiss Ephemeris library, which provides high-precision astronomical calculations for astrological computations.

## Project Status

**Status:** Prototype

**Development Period:** March 2025

## Key Features

### Core Functionality

- **Planetary Position Calculation**: Computes positions for all major planets
- **Vedic (Sidereal) Zodiac**: Uses Lahiri Ayanamsa for Vedic calculations
- **Birth Chart Visualization**: Interactive chart display
- **Planetary Positions in Signs**: Detailed position information
- **Lunar Nodes**: Includes Rahu and Ketu calculations
- **Timezone Support**: Handles different timezones correctly
- **House System**: Equal House system for house cusps

### Astronomical Features

- **Swiss Ephemeris Integration**: High-precision calculations
- **Sidereal Zodiac**: Vedic astrology calculations
- **Planetary Positions**: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Rahu, Ketu
- **House Cusps**: Equal House system
- **Longitude/Latitude Support**: Accurate location-based calculations

## Technology Stack

### Backend
- **Framework**: Flask
- **Astronomical Library**: Swiss Ephemeris (pyswisseph)
- **Templates**: Jinja2
- **Forms**: Flask-WTF

### Astronomical Calculations
- **Swiss Ephemeris**: High-precision ephemeris data
- **Ayanamsa**: Lahiri Ayanamsa for Vedic calculations
- **Coordinate Systems**: Ecliptic coordinates
- **Time Calculations**: UTC conversion and timezone handling

## Architecture

### Application Structure

```
vedic_astrology/
├── app.py                 # Main Flask application
├── templates/            # Jinja2 templates
│   └── chart.html        # Birth chart display
├── static/                # CSS, JS
└── requirements.txt      # Dependencies
```

### Calculation Flow

```mermaid
graph LR
    User[User Input] --> Form[Birth Data Form]
    Form --> Validation[Input Validation]
    Validation --> Swiss[Swiss Ephemeris]
    Swiss --> Calculation[Planetary Calculations]
    Calculation --> Ayanamsa[Ayanamsa Correction]
    Ayanamsa --> Positions[Planetary Positions]
    Positions --> Houses[House Calculations]
    Houses --> Chart[Chart Generation]
    Chart --> Display[Visualization]
```

## Swiss Ephemeris Integration

### Key Features

- **High Precision**: Swiss Ephemeris provides accurate planetary positions
- **Ephemeris Data**: Requires ephemeris data files
- **Multiple Bodies**: Supports planets, asteroids, and fixed stars
- **Time Range**: Extensive historical and future date support

### Calculation Process

1. **Input Processing**: Birth date, time, location, timezone
2. **UTC Conversion**: Convert local time to UTC
3. **Julian Day Calculation**: Convert to Julian Day Number
4. **Planetary Positions**: Calculate positions using Swiss Ephemeris
5. **Ayanamsa Application**: Apply Lahiri Ayanamsa for sidereal zodiac
6. **House Calculation**: Compute house cusps using Equal House system
7. **Chart Generation**: Create visualization data

## Planetary Calculations

### Supported Bodies

- **Sun**: Solar position
- **Moon**: Lunar position
- **Mercury**: Inner planet
- **Venus**: Inner planet
- **Mars**: Outer planet
- **Jupiter**: Outer planet
- **Saturn**: Outer planet
- **Rahu**: North lunar node
- **Ketu**: South lunar node

### Position Information

For each planet, the calculator provides:
- **Longitude**: Position in degrees
- **Sign**: Zodiac sign (Aries through Pisces)
- **Degree in Sign**: Exact position within sign
- **House**: House placement

## Vedic Astrology Specifics

### Ayanamsa

- **Lahiri Ayanamsa**: Standard for Vedic astrology
- **Sidereal Zodiac**: Fixed star-based zodiac
- **Precession Correction**: Accounts for Earth's precession

### House System

- **Equal House**: Each house is 30 degrees
- **Ascendant-Based**: Houses calculated from Ascendant
- **House Cusps**: Exact degree positions

## User Interface

### Input Form

- Birth date (day, month, year)
- Birth time (24-hour format)
- Latitude (positive for North, negative for South)
- Longitude (positive for East, negative for West)
- Timezone selection

### Output Display

- **Birth Chart Visualization**: Circular chart display
- **Planetary Positions Table**: Detailed position information
- **House Positions**: House cusps and planetary house placements

## Project Statistics

| Metric | Value |
|--------|-------|
| **Python Files** | 2+ |
| **Templates** | 1+ |
| **Planets Calculated** | 9 (Sun, Moon, 5 planets, 2 nodes) |
| **House System** | Equal House |

## Code Samples

See the [code-samples](./code-samples/) directory for examples of:
- Swiss Ephemeris integration
- Birth chart calculations
- Planetary position computation
- Chart visualization

## Case Studies

- [Swiss Ephemeris Integration](./case-studies/swiss-ephemeris-integration.md)

---

**Note:** This is a showcase repository. The actual production codebase remains private.

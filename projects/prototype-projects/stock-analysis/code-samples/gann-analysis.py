"""
Gann Analysis for Stock Technical Analysis
Demonstrates Gann theory implementation for trend identification.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calculate_gann_line(data, angle=1):
    """
    Calculate Gann line based on Gann angles.
    
    Args:
        data: DataFrame with 'Close' prices
        angle: Gann angle (1 = 45 degrees, 2 = 26.25 degrees, etc.)
    
    Returns:
        Gann line values
    """
    # Get first price point
    first_price = data['Close'].iloc[0]
    first_index = data.index[0]
    
    # Calculate price increment per unit (for 45-degree angle)
    # Gann angle of 1 means 1 unit of price per 1 unit of time
    price_range = data['Close'].max() - data['Close'].min()
    time_range = len(data)
    
    # Calculate increment based on angle
    increment = (price_range / time_range) * angle
    
    # Generate Gann line
    gann_line = []
    for i in range(len(data)):
        gann_value = first_price + (i * increment)
        gann_line.append(gann_value)
    
    return np.array(gann_line)

def identify_support_resistance(data, window=20):
    """
    Identify support and resistance levels using Gann principles.
    
    Args:
        data: DataFrame with 'High', 'Low', 'Close' prices
        window: Window size for local extrema
    
    Returns:
        support_levels: List of support levels
        resistance_levels: List of resistance levels
    """
    highs = data['High'].rolling(window=window).max()
    lows = data['Low'].rolling(window=window).min()
    
    # Find local maxima (resistance)
    resistance_levels = []
    for i in range(window, len(data) - window):
        if data['High'].iloc[i] == highs.iloc[i]:
            resistance_levels.append(data['High'].iloc[i])
    
    # Find local minima (support)
    support_levels = []
    for i in range(window, len(data) - window):
        if data['Low'].iloc[i] == lows.iloc[i]:
            support_levels.append(data['Low'].iloc[i])
    
    # Remove duplicates and sort
    support_levels = sorted(list(set(support_levels)))
    resistance_levels = sorted(list(set(resistance_levels)))
    
    return support_levels, resistance_levels

def plot_gann_analysis(data, ticker, angle=1):
    """
    Plot stock prices with Gann analysis overlay.
    
    Args:
        data: DataFrame with stock data
        ticker: Stock ticker symbol
        angle: Gann angle
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot closing prices
    ax.plot(data.index, data['Close'], label='Close Price', linewidth=2)
    
    # Calculate and plot Gann line
    gann_line = calculate_gann_line(data, angle)
    ax.plot(data.index, gann_line, label=f'Gann Line (Angle {angle})', 
            linestyle='--', linewidth=2, color='red')
    
    # Identify and plot support/resistance
    support_levels, resistance_levels = identify_support_resistance(data)
    
    # Plot key support/resistance levels
    for level in support_levels[-3:]:  # Last 3 support levels
        ax.axhline(y=level, color='green', linestyle=':', alpha=0.5, label='Support' if level == support_levels[-3] else '')
    
    for level in resistance_levels[-3:]:  # Last 3 resistance levels
        ax.axhline(y=level, color='red', linestyle=':', alpha=0.5, label='Resistance' if level == resistance_levels[-3] else '')
    
    ax.set_title(f'{ticker} Stock Price with Gann Analysis')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

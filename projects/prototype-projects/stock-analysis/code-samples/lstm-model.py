"""
LSTM Model for Stock Price Prediction
Demonstrates time series forecasting with LSTM neural networks.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

def prepare_data(data, window_size=60):
    """
    Prepare data for LSTM model using sliding window approach.
    
    Args:
        data: DataFrame with 'Close' prices
        window_size: Number of time steps to look back
    
    Returns:
        X: Input sequences
        y: Target values
        scaler: Fitted scaler for inverse transformation
    """
    # Extract closing prices
    prices = data['Close'].values.reshape(-1, 1)
    
    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_prices = scaler.fit_transform(prices)
    
    # Create sequences
    X, y = [], []
    for i in range(window_size, len(scaled_prices)):
        X.append(scaled_prices[i-window_size:i, 0])
        y.append(scaled_prices[i, 0])
    
    X, y = np.array(X), np.array(y)
    
    # Reshape for LSTM (samples, time steps, features)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    return X, y, scaler

def create_lstm_model(input_shape, units=50, dropout=0.2):
    """
    Create LSTM model for stock price prediction.
    
    Args:
        input_shape: Shape of input data (time_steps, features)
        units: Number of LSTM units
        dropout: Dropout rate
    
    Returns:
        Compiled LSTM model
    """
    model = Sequential([
        # First LSTM layer
        LSTM(units=units, return_sequences=True, input_shape=input_shape),
        Dropout(dropout),
        
        # Second LSTM layer
        LSTM(units=units, return_sequences=True),
        Dropout(dropout),
        
        # Third LSTM layer
        LSTM(units=units, return_sequences=False),
        Dropout(dropout),
        
        # Dense output layer
        Dense(units=1)
    ])
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='mean_squared_error',
        metrics=['mean_absolute_error']
    )
    
    return model

def train_model(model, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
    """
    Train the LSTM model.
    
    Args:
        model: LSTM model
        X_train: Training input sequences
        y_train: Training target values
        X_val: Validation input sequences
        y_val: Validation target values
        epochs: Number of training epochs
        batch_size: Batch size for training
    
    Returns:
        Training history
    """
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )
    
    return history

def predict_future_prices(model, last_sequence, scaler, days=30):
    """
    Predict future stock prices.
    
    Args:
        model: Trained LSTM model
        last_sequence: Last window_size days of prices
        scaler: Fitted scaler
        days: Number of days to predict
    
    Returns:
        Predicted prices (denormalized)
    """
    predictions = []
    current_sequence = last_sequence.copy()
    
    for _ in range(days):
        # Predict next value
        next_pred = model.predict(current_sequence.reshape(1, current_sequence.shape[0], 1))
        predictions.append(next_pred[0, 0])
        
        # Update sequence (sliding window)
        current_sequence = np.append(current_sequence[1:], next_pred[0, 0])
    
    # Denormalize predictions
    predictions = np.array(predictions).reshape(-1, 1)
    predictions = scaler.inverse_transform(predictions)
    
    return predictions.flatten()

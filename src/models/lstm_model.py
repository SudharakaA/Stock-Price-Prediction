"""
LSTM neural network model for stock price prediction.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from typing import Tuple, Optional
import joblib
import os


class LSTMPredictor:
    """
    LSTM model for stock price prediction.
    """
    
    def __init__(self, sequence_length: int = 60, features: list = None):
        """
        Initialize LSTM predictor.
        
        Args:
            sequence_length: Number of time steps to look back
            features: List of features to use for prediction
        """
        self.sequence_length = sequence_length
        self.features = features or ['Open', 'High', 'Low', 'Close', 'Volume']
        self.model = None
        self.scaler = MinMaxScaler()
        self.is_trained = False
        
    def prepare_data(self, df: pd.DataFrame, target_column: str = 'Close') -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare data for LSTM training.
        
        Args:
            df: DataFrame with stock data
            target_column: Column to predict
            
        Returns:
            Tuple of (X, y) arrays
        """
        # Select features that exist in the dataframe
        available_features = [col for col in self.features if col in df.columns]
        
        if not available_features:
            raise ValueError(f"None of the specified features {self.features} are available in the data")
        
        # Use available features
        data = df[available_features].values
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(data)
        
        # Create sequences
        X, y = [], []
        target_idx = available_features.index(target_column)
        
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i])
            y.append(scaled_data[i, target_idx])
        
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape: Tuple) -> Sequential:
        """
        Build LSTM model architecture.
        
        Args:
            input_shape: Shape of input data
            
        Returns:
            Compiled Keras model
        """
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(1)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        return model
    
    def train(self, df: pd.DataFrame, target_column: str = 'Close', 
              validation_split: float = 0.2, epochs: int = 50, batch_size: int = 32) -> dict:
        """
        Train the LSTM model.
        
        Args:
            df: Training data
            target_column: Column to predict
            validation_split: Validation data split
            epochs: Number of training epochs
            batch_size: Training batch size
            
        Returns:
            Training history
        """
        # Prepare data
        X, y = self.prepare_data(df, target_column)
        
        # Build model
        self.model = self.build_model((X.shape[1], X.shape[2]))
        
        # Train model
        history = self.model.fit(
            X, y,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        
        self.is_trained = True
        return history.history
    
    def predict(self, df: pd.DataFrame, days_ahead: int = 1) -> np.ndarray:
        """
        Make predictions using the trained model.
        
        Args:
            df: Input data for prediction
            days_ahead: Number of days to predict ahead
            
        Returns:
            Predicted values (unscaled)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Prepare the last sequence for prediction
        available_features = [col for col in self.features if col in df.columns]
        data = df[available_features].tail(self.sequence_length).values
        scaled_data = self.scaler.transform(data)
        
        predictions = []
        current_sequence = scaled_data.copy()
        
        for _ in range(days_ahead):
            # Reshape for prediction
            X = current_sequence.reshape(1, self.sequence_length, len(available_features))
            
            # Make prediction
            pred_scaled = self.model.predict(X, verbose=0)[0, 0]
            predictions.append(pred_scaled)
            
            # Update sequence for next prediction
            new_row = current_sequence[-1].copy()
            target_idx = available_features.index('Close')
            new_row[target_idx] = pred_scaled
            
            current_sequence = np.vstack([current_sequence[1:], new_row])
        
        # Create dummy array for inverse transform
        dummy_array = np.zeros((len(predictions), len(available_features)))
        target_idx = available_features.index('Close')
        dummy_array[:, target_idx] = predictions
        
        # Inverse transform to get actual prices
        unscaled_predictions = self.scaler.inverse_transform(dummy_array)[:, target_idx]
        
        return unscaled_predictions
    
    def evaluate(self, df: pd.DataFrame, target_column: str = 'Close') -> dict:
        """
        Evaluate model performance.
        
        Args:
            df: Test data
            target_column: Target column to evaluate
            
        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
        
        # Prepare test data
        X, y_true = self.prepare_data(df, target_column)
        
        # Make predictions
        y_pred = self.model.predict(X, verbose=0).flatten()
        
        # Calculate metrics
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        
        # Calculate MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        return {
            'mse': mse,
            'mae': mae,
            'rmse': rmse,
            'mape': mape
        }
    
    def save_model(self, filepath: str):
        """
        Save the trained model and scaler.
        
        Args:
            filepath: Path to save the model (without extension)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        # Save model
        self.model.save(f"{filepath}_model.h5")
        
        # Save scaler
        joblib.dump(self.scaler, f"{filepath}_scaler.pkl")
        
        # Save configuration
        config = {
            'sequence_length': self.sequence_length,
            'features': self.features
        }
        joblib.dump(config, f"{filepath}_config.pkl")
    
    def load_model(self, filepath: str):
        """
        Load a saved model and scaler.
        
        Args:
            filepath: Path to the saved model (without extension)
        """
        # Load model
        self.model = tf.keras.models.load_model(f"{filepath}_model.h5")
        
        # Load scaler
        self.scaler = joblib.load(f"{filepath}_scaler.pkl")
        
        # Load configuration
        config = joblib.load(f"{filepath}_config.pkl")
        self.sequence_length = config['sequence_length']
        self.features = config['features']
        
        self.is_trained = True
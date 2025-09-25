"""
Prophet model for stock price prediction.
"""

import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class ProphetPredictor:
    """
    Prophet model for stock price prediction using Facebook's Prophet library.
    """
    
    def __init__(self):
        """Initialize Prophet predictor."""
        self.model = None
        self.is_trained = False
        
    def prepare_data(self, df: pd.DataFrame, target_column: str = 'Close') -> pd.DataFrame:
        """
        Prepare data for Prophet training.
        Prophet requires 'ds' (date) and 'y' (target) columns.
        
        Args:
            df: DataFrame with stock data
            target_column: Column to predict
            
        Returns:
            DataFrame formatted for Prophet
        """
        prophet_df = pd.DataFrame()
        prophet_df['ds'] = pd.to_datetime(df['Date'])
        prophet_df['y'] = df[target_column]
        
        # Remove any rows with missing values
        prophet_df = prophet_df.dropna()
        
        return prophet_df
    
    def add_regressors(self, df: pd.DataFrame, prophet_df: pd.DataFrame, 
                      additional_features: list = None) -> pd.DataFrame:
        """
        Add additional regressors to Prophet data.
        
        Args:
            df: Original DataFrame with stock data
            prophet_df: Prophet-formatted DataFrame
            additional_features: List of additional features to include
            
        Returns:
            Prophet DataFrame with additional regressors
        """
        if additional_features is None:
            additional_features = ['Volume', 'High', 'Low', 'Open']
        
        for feature in additional_features:
            if feature in df.columns:
                prophet_df[feature] = df[feature].values[:len(prophet_df)]
        
        return prophet_df
    
    def train(self, df: pd.DataFrame, target_column: str = 'Close', 
              additional_features: list = None, **prophet_params) -> None:
        """
        Train the Prophet model.
        
        Args:
            df: Training data
            target_column: Column to predict
            additional_features: Additional features to include as regressors
            **prophet_params: Additional parameters for Prophet model
        """
        # Set default Prophet parameters
        default_params = {
            'daily_seasonality': True,
            'weekly_seasonality': True,
            'yearly_seasonality': True,
            'changepoint_prior_scale': 0.05,
            'seasonality_prior_scale': 10.0,
            'interval_width': 0.8
        }
        default_params.update(prophet_params)
        
        # Initialize model
        self.model = Prophet(**default_params)
        
        # Prepare data
        prophet_df = self.prepare_data(df, target_column)
        
        # Add additional regressors if specified
        if additional_features:
            prophet_df = self.add_regressors(df, prophet_df, additional_features)
            for feature in additional_features:
                if feature in prophet_df.columns:
                    self.model.add_regressor(feature)
        
        # Fit the model
        self.model.fit(prophet_df)
        self.is_trained = True
        
    def predict(self, df: pd.DataFrame, days_ahead: int = 30, 
                additional_features: list = None) -> pd.DataFrame:
        """
        Make predictions using the trained Prophet model.
        
        Args:
            df: Input data for prediction
            days_ahead: Number of days to predict ahead
            additional_features: Additional features used during training
            
        Returns:
            DataFrame with predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=days_ahead)
        
        # Add regressors for future predictions if they were used in training
        if additional_features:
            # For simplicity, use the last known values for additional features
            # In practice, you might want to predict these features separately
            last_values = df[additional_features].iloc[-1]
            for feature in additional_features:
                if feature in df.columns:
                    # Extend the feature values (using last known value)
                    feature_values = list(df[feature]) + [last_values[feature]] * days_ahead
                    future[feature] = feature_values[:len(future)]
        
        # Make predictions
        forecast = self.model.predict(future)
        
        return forecast
    
    def cross_validate_model(self, df: pd.DataFrame, target_column: str = 'Close',
                           initial: str = '365 days', period: str = '90 days', 
                           horizon: str = '30 days') -> pd.DataFrame:
        """
        Perform cross-validation on the model.
        
        Args:
            df: Data for cross-validation
            target_column: Target column
            initial: Initial training period
            period: Period between cutoff dates
            horizon: Forecast horizon
            
        Returns:
            Cross-validation results
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before cross-validation")
        
        # Prepare data
        prophet_df = self.prepare_data(df, target_column)
        
        # Perform cross-validation
        cv_results = cross_validation(
            self.model, 
            initial=initial, 
            period=period, 
            horizon=horizon,
            parallel="processes"
        )
        
        return cv_results
    
    def evaluate(self, df: pd.DataFrame, target_column: str = 'Close') -> Dict:
        """
        Evaluate model performance using cross-validation.
        
        Args:
            df: Test data
            target_column: Target column
            
        Returns:
            Dictionary with evaluation metrics
        """
        try:
            # Perform cross-validation
            cv_results = self.cross_validate_model(df, target_column)
            
            # Calculate performance metrics
            metrics = performance_metrics(cv_results)
            
            # Return summary statistics
            return {
                'mae': metrics['mae'].mean(),
                'mape': metrics['mape'].mean(),
                'rmse': metrics['rmse'].mean(),
                'coverage': metrics['coverage'].mean()
            }
        except Exception as e:
            print(f"Error in evaluation: {e}")
            return {}
    
    def get_components(self, forecast: pd.DataFrame) -> pd.DataFrame:
        """
        Get forecast components (trend, seasonality, etc.).
        
        Args:
            forecast: Forecast results from predict()
            
        Returns:
            DataFrame with forecast components
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting components")
        
        components = self.model.predict(forecast[['ds']])
        return components
    
    def detect_changepoints(self) -> pd.DataFrame:
        """
        Detect significant changepoints in the time series.
        
        Returns:
            DataFrame with changepoint information
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before detecting changepoints")
        
        changepoints = pd.DataFrame({
            'changepoint': self.model.changepoints,
            'delta': self.model.params['delta'].mean(axis=0)
        })
        
        # Sort by absolute delta value to find most significant changepoints
        changepoints['abs_delta'] = np.abs(changepoints['delta'])
        changepoints = changepoints.sort_values('abs_delta', ascending=False)
        
        return changepoints
    
    def plot_forecast(self, forecast: pd.DataFrame, save_path: Optional[str] = None):
        """
        Plot the forecast results.
        
        Args:
            forecast: Forecast results
            save_path: Optional path to save the plot
        """
        try:
            import matplotlib.pyplot as plt
            
            fig = self.model.plot(forecast)
            plt.title('Stock Price Prediction using Prophet')
            plt.xlabel('Date')
            plt.ylabel('Price')
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
            plt.show()
            
        except ImportError:
            print("Matplotlib not available for plotting")
    
    def plot_components(self, forecast: pd.DataFrame, save_path: Optional[str] = None):
        """
        Plot forecast components.
        
        Args:
            forecast: Forecast results
            save_path: Optional path to save the plot
        """
        try:
            import matplotlib.pyplot as plt
            
            fig = self.model.plot_components(forecast)
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
            plt.show()
            
        except ImportError:
            print("Matplotlib not available for plotting")
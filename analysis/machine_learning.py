import pandas as pd
import numpy as np
import statsmodels.api as sm
import plotly.express as px
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX

def train_model(data, forecast_periods=12):
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data = data.dropna(subset=['Date'])

    # Aggregate monthly sales
    data['YearMonth'] = data['Date'].dt.to_period('M')
    monthly_sales = data.groupby('YearMonth')[['Sales', 'Profit']].sum().reset_index()
    monthly_sales['Date'] = monthly_sales['YearMonth'].dt.to_timestamp()

    # Ensure continuity of dates
    all_months = pd.date_range(start=monthly_sales['Date'].min(), end=monthly_sales['Date'].max(), freq='MS')
    all_months_df = pd.DataFrame({'Date': all_months})
    monthly_sales = all_months_df.merge(monthly_sales, on='Date', how='left').fillna({'Sales': 0, 'Profit': 0})

    # Augmented Dickey-Fuller Test for stationarity
    def adfuller_test(series):
        return adfuller(series)[1]  # Return p-value

    d_sales, d_profit = 0, 0
    sales_series, profit_series = monthly_sales['Sales'], monthly_sales['Profit']
    leg_sales, leg_profit = adfuller(sales_series)[2], adfuller(profit_series)[2]

    while adfuller_test(sales_series) > 0.05:
        sales_series = sales_series.diff().dropna()
        leg_sales = adfuller(sales_series)[2]
        d_sales += 1
    while adfuller_test(profit_series) > 0.05:
        profit_series = profit_series.diff().dropna()
        leg_profit = adfuller(profit_series)[2]
        d_profit += 1

    # Compute ACF and PACF values
    acf_sales_values = acf(monthly_sales['Sales'].dropna(), nlags=leg_sales)
    pacf_sales_values = pacf(monthly_sales['Sales'].dropna(), nlags=leg_sales)
    acf_profit_values = acf(monthly_sales['Profit'].dropna(), nlags=leg_profit)
    pacf_profit_values = pacf(monthly_sales['Profit'].dropna(), nlags=leg_profit)

    p_sales = next((i for i, val in enumerate(pacf_sales_values) if abs(val) < 0.2), 1)
    q_sales = next((i for i, val in enumerate(acf_sales_values) if abs(val) < 0.2), 1)
    p_profit = next((i for i, val in enumerate(pacf_profit_values) if abs(val) < 0.2), 1)
    q_profit = next((i for i, val in enumerate(acf_profit_values) if abs(val) < 0.2), 1)

    # Train SARIMA models
    sales1 = monthly_sales.set_index('Date')
    sarima_sales_model = SARIMAX(sales1['Sales'], order=(p_sales, d_sales, q_sales), seasonal_order=(p_sales, d_sales, q_sales, 12))
    sarima_sales_result = sarima_sales_model.fit()
    sarima_profit_model = SARIMAX(sales1['Profit'], order=(p_profit, d_profit, q_profit), seasonal_order=(p_profit, d_profit, q_profit, 12))
    sarima_profit_result = sarima_profit_model.fit()

    # Generate future dates for forecast
    future_dates = pd.date_range(start=sales1.index[-1] + pd.DateOffset(months=1), 
                                 periods=forecast_periods, freq='MS')
    future_df = pd.DataFrame(index=future_dates)

    # Forecast for future periods only
    future_df['SARIMA_Sales_Forecast'] = sarima_sales_result.forecast(steps=forecast_periods)
    future_df['SARIMA_Profit_Forecast'] = sarima_profit_result.forecast(steps=forecast_periods)

    fig1 = px.line(x=future_df.index, y=future_df['SARIMA_Sales_Forecast'], 
                   title="Forecasting of Sales", template="plotly_dark", 
                   labels={'x': 'Date', 'y': 'Sales'})
    
    fig2 = px.line(x=future_df.index, y=future_df['SARIMA_Profit_Forecast'], 
                   title="Forecasting of Profit", template="plotly_dark", 
                   labels={'x': 'Date', 'y': 'Profit'}, 
                   line_shape='linear', line_dash_sequence=['solid'])
    fig2.update_traces(line=dict(color='green'))


    return fig1.to_html(), fig2.to_html()
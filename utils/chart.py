import streamlit as st
import plotly.graph_objects as go
import mplfinance as mpf
import pandas as pd

def plot_candlestick_chart_plotly(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    
     # Add markers: LONG ⬇️), SHORT (⬆️), NONE (🟡)
    if 'signal' in df.columns:
        long_signals = df[df['signal'] == 'LONG']
        short_signals = df[df['signal'] == 'SHORT']
        none_signals = df[df['signal'] == 'NONE']

        # Green Down Arrows for LONG (below low)
        fig.add_trace(go.Scatter(
            x=long_signals['timestamp'],
            y=long_signals['low'] - 2,  # Adjust marker position
            mode='markers',
            marker=dict(symbol='arrow-down', color='green', size=12),
            name='LONG'
        ))

        # Red Up Arrows for SHORT (above high)
        fig.add_trace(go.Scatter(
            x=short_signals['timestamp'],
            y=short_signals['high'] + 2,  # Adjust marker position
            mode='markers',
            marker=dict(symbol='arrow-up', color='red', size=12),
            name='SHORT'
        ))

        # Yellow Circles for NONE (at close)
        fig.add_trace(go.Scatter(
            x=none_signals['timestamp'],
            y=none_signals['close'],
            mode='markers',
            marker=dict(symbol='circle', color='yellow', size=8),
            name='NONE'
        ))

    fig.update_layout(
        title='TSLA Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_candlestick_chart_mpf(df):
    df.index = pd.DatetimeIndex(df['timestamp'])
    fig, ax = mpf.plot(
        df,
        type='candle',
        style='charles',
        returnfig=True,
        volume=False,
        figsize=(10,6)
    )
    st.pyplot(fig)

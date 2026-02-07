import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="StockVision Pro", layout="wide", page_icon="💹")

# 2. Advanced Dark Theme & White Box CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0a0b10;
    }
    
    /* Metric Card Styling - White Glassmorphism */
    [data-testid="stMetricValue"] {
        color: #1f1f1f !important;
    }
    [data-testid="stMetricLabel"] {
        color: #4f4f4f !important;
    }
    div[data-testid="column"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 10px;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #161b22;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Load Data
@st.cache_data
def load_data():
    # Ensure your path is correct
    df = pd.read_csv("../yfinance_Project/Stock_NS.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
    
    # 4. Sidebar Controls
    st.sidebar.header("🛠 Control Panel")
    stock_list = df['Stock'].unique()
    selected_stock = st.sidebar.selectbox("Choose Stock", stock_list)
    
    window = st.sidebar.slider("Moving Average Window (Days)", 5, 50, 20)
    
    # Filter Data
    r = df[df['Stock'] == selected_stock].sort_values('Date')
    
    # Calculate Moving Average
    r['MA'] = r['Close'].rolling(window=window).mean()

    # 5. Header
    st.title(f"🚀 {selected_stock} Analysis Dashboard")
    st.markdown("---")

    # 6. Metrics Section (Now in White Boxes)
    latest_price = r['Close'].iloc[-1]
    prev_price = r['Close'].iloc[-2]
    high_price = r['Close'].max()
    low_price = r['Close'].min()
    delta = ((latest_price - prev_price) / prev_price) * 100

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Current Close", f"₹{latest_price:,.2f}", f"{delta:+.2f}%")
    with m2:
        st.metric("Period High", f"₹{high_price:,.2f}")
    with m3:
        st.metric("Period Low", f"₹{low_price:,.2f}")

    # 7. Candlestick Chart with Zoom
    st.subheader("Price Action & Trends")
    
    fig = go.Figure()

    # Add Candlestick
    # Note: If your CSV doesn't have Open/High/Low, this uses Close for all
    # For better results, ensure your CSV has 'Open', 'High', 'Low', 'Close'
    fig.add_trace(go.Candlestick(
        x=r['Date'],
        open=r['Close'], # Replace with r['Open'] if available
        high=r['Close'], # Replace with r['High'] if available
        low=r['Close'],  # Replace with r['Low'] if available
        close=r['Close'],
        name='Market Price'
    ))

    # Add Moving Average Line
    fig.add_trace(go.Scatter(
        x=r['Date'], 
        y=r['MA'], 
        line=dict(color='#FFD700', width=2), 
        name=f'{window}-Day MA'
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=True, # Built-in Zoom tool
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Stock Price (INR)",
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 8. Extra Features: Volume Analysis
    st.subheader("Volume Insights")
    fig_vol = go.Figure(go.Bar(x=r.Date, y=r.get('Volume', [0]*len(r)), marker_color='#00ffcc'))
    fig_vol.update_layout(template="plotly_dark", height=200, margin=dict(t=0, b=0))
    st.plotly_chart(fig_vol, use_container_width=True)

except Exception as e:
    st.error(f"Analysis Error: {e}")

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Stock Analytics Pro", layout="wide", initial_sidebar_state="expanded")

# 2. Custom CSS for "Cool" Dark Aesthetics
st.markdown("""
    <style>
    .main {
        background-color: ##fff152;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e4250;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Loading (Cached for speed)
@st.cache_data
def load_data():
    df = pd.read_csv("Stock_NS.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()

    # 4. Sidebar - Controls
    st.sidebar.header("📈 Dashboard Controls")
    stock_list = df['Stock'].unique()
    selected_stock = st.sidebar.selectbox("Select Stock Symbol", stock_list)

    # Filter Data
    r = df[df['Stock'] == selected_stock].sort_values('Date')

    # 5. Main UI Layout
    st.title(f"🚀 {selected_stock} Performance Analysis")
    st.markdown(f"Visualizing historical data for **{selected_stock}**")

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    current_price = r['Close'].iloc[-1]
    prev_price = r['Close'].iloc[-2]
    delta = ((current_price - prev_price) / prev_price) * 100

    col1.metric("Current Close", f"₹{current_price:,.2f}", f"{delta:+.2f}%")
    col2.metric("High (Period)", f"₹{r['Close'].max():,.2f}")
    col3.metric("Low (Period)", f"₹{r['Close'].min():,.2f}")

    st.divider()

    # 6. Interactive Plotting
    fig = px.line(r, x='Date', y='Close', 
                  title=f"{selected_stock} Closing Price Trend",
                  template="plotly_dark",
                  color_discrete_sequence=['#00d4ff'])

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Price (INR)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    st.plotly_chart(fig, use_container_width=True)

    # 7. Data Preview Toggle
    with st.expander("View Raw Data"):
        st.dataframe(r.style.background_gradient(subset=['Close'], cmap='BuGn'), use_container_width=True)

except FileNotFoundError:
    st.error("CSV file not found. Please check the file path: `../yfinance_Project/Stock_NS.csv`")

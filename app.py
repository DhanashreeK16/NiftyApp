import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Stock Analytics Pro", layout="wide", page_icon="📈")

# 2. Custom CSS for Styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    div.stButton > button:first-child {
        background-color: #00ffcc;
        color: black;
        border-radius: 10px;
    }
    .metric-container {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #31333f;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Stock_NS.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()

    # 4. Sidebar Navigation
    st.sidebar.title("🚀 Stock Explorer")
    stock_list = df['Stock'].unique()
    selected_stock = st.sidebar.selectbox("Select Stock Ticker", stock_list)
    
    # Filter Data
    r = df[df['Stock'] == selected_stock].sort_values('Date')

    # 5. Dashboard Header
    st.title(f"📊 {selected_stock} Performance Dashboard")
    
    # 6. Key Metrics Row
    col1, col2, col3 = st.columns(3)
    latest_price = r['Close'].iloc[-1]
    prev_price = r['Close'].iloc[-2]
    delta = ((latest_price - prev_price) / prev_price) * 100

    col1.metric("Current Price", f"₹{latest_price:,.2f}", f"{delta:+.2f}%")
    col2.metric("High (Period)", f"₹{r['Close'].max():,.2f}")
    col3.metric("Low (Period)", f"₹{r['Close'].min():,.2f}")

    st.divider()

    # 7. Interactive Chart (Plotly)
    st.subheader("Price History (Interactive Zoom & Pan)")
    
    fig = px.line(r, x='Date', y='Close', 
                  template="plotly_dark",
                  color_discrete_sequence=['#00ffcc'])
    
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Timeline",
        yaxis_title="Closing Price",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    
    # Adding Range Slider for Zooming
    fig.update_xaxes(rangeslider_visible=True)
    
    st.plotly_chart(fig, use_container_width=True)

    # 8. Data Statistics & Table
    with st.expander("View Raw Data and Summary Statistics"):
        tab1, tab2 = st.tabs(["📊 Statistics", "📂 Dataset"])
        with tab1:
            st.write(r.describe())
        with tab2:
            st.dataframe(r, use_container_width=True)

except Exception as e:
    st.error(f"Error loading file: {e}")
    st.info("Ensure 'Stock_NS.csv' is in the correct directory.")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyspark.sql import SparkSession
import numpy as np

st.set_page_config(layout="wide")

st.title("Finance Dashboard")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Nifty 50", "49500", "0.8%")
with col2:
    st.metric("Portfolio", "1250000", "+15000")
with col3:
    st.metric("Daily PnL", "1.2%", "+1.2%")

spark = SparkSession.builder.appName("Dashboard").getOrCreate()

@st.cache_data(ttl=300)
def load_data():
    features = spark.read.parquet("data_lake/processed/features/").limit(10000).toPandas()
    portfolio = spark.read.parquet("data_lake/processed/portfolio/").toPandas()
    return features, portfolio

features, portfolio = load_data()

col1, col2 = st.columns(2)
with col1:
    fig = px.line(features.sample(5000), x="timestamp", y="returns", 
                  title="Returns", color="symbol")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.bar(portfolio, x="user_id", y="total_spent", 
                  title="Spending by User")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("💾 Big Data Stats")
st.write(f"**Processed:** {len(features):,} rows with Spark")
st.write(f"**Features:** Returns, hourly trends, portfolio metrics")
st.caption("🔄 Updates every 5min • FREE market data")

spark.stop()

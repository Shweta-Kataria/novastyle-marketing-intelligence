import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load and clean data
df = pd.read_csv('marketing_campaign.csv', sep=';')
df['Income'] = df['Income'].fillna(df['Income'].median())

# Create KPIs
df['TotalSpend'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
df['TotalPurchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases']
df['TotalCampaignsAccepted'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5']
df['Age'] = 2025 - df['Year_Birth']
df['EngagementScore'] = df['TotalSpend'] + (df['TotalPurchases'] * 10) + (df['TotalCampaignsAccepted'] * 20)

# Page config
st.set_page_config(page_title="NovaStyle Marketing Intelligence", layout="wide")

# Title
st.title("🛍️ NovaStyle Marketing Intelligence System")
st.markdown("AI-powered marketing analytics dashboard")

# Section 1 — Executive KPIs
st.header("📊 Executive KPIs")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(df):,}")
col2.metric("Avg Customer Spend", f"${df['TotalSpend'].mean():.0f}")
col3.metric("Avg Income", f"${df['Income'].mean():.0f}")
col4.metric("Campaign Response Rate", f"{df['Response'].mean()*100:.1f}%")

# Section 2 — Channel Performance
st.header("📣 Campaign Performance by Channel")
campaign_data = {
    'Channel': ['Google Ads', 'Instagram', 'TikTok', 'Email', 'Catalogue'],
    'Acceptance Rate': [
        df['AcceptedCmp1'].mean()*100,
        df['AcceptedCmp2'].mean()*100,
        df['AcceptedCmp3'].mean()*100,
        df['AcceptedCmp4'].mean()*100,
        df['AcceptedCmp5'].mean()*100
    ]
}
st.bar_chart(pd.DataFrame(campaign_data).set_index('Channel'))

# Section 3 — Spend by Education
st.header("🎓 Average Spend by Education Level")
edu_spend = df.groupby('Education')['TotalSpend'].mean()
st.bar_chart(edu_spend)

# Section 4 — AI Recommendations
st.header("🤖 AI Strategic Recommendations")
with open('ai_recommendations.txt', 'r') as f:
    recommendations = f.read()
st.info(recommendations)

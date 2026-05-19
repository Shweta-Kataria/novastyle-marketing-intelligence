import os
import pandas as pd
import streamlit as st
from openai import OpenAI

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

# Section 4 — AI Recommendations (Auto-generated from live data)
st.header("🤖 AI Strategic Recommendations")
st.markdown("*Generated automatically from latest data*")

# Build summary from current data
summary = f"""
Customer Dataset Summary:
- Total Customers: {len(df)}
- Average Income: ${df['Income'].mean():.0f}
- Average Total Spend: ${df['TotalSpend'].mean():.0f}

Campaign Acceptance Rates:
- Google Ads: {df['AcceptedCmp1'].mean()*100:.1f}%
- Instagram: {df['AcceptedCmp2'].mean()*100:.1f}%
- TikTok: {df['AcceptedCmp3'].mean()*100:.1f}%
- Email: {df['AcceptedCmp4'].mean()*100:.1f}%
- Catalogue: {df['AcceptedCmp5'].mean()*100:.1f}%

Top Spending Education Level: {df.groupby('Education')['TotalSpend'].mean().idxmax()}
Top Spending Age Group: 70+
"""

# Generate insights button
if st.button("🔄 Generate Fresh AI Insights"):
    with st.spinner("Analyzing data and generating recommendations..."):
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"You are a senior marketing analyst. Analyze this data and give 5 executive recommendations:\n{summary}"
            }]
        )
        recommendations = response.choices[0].message.content
        
        # Save to file
        with open('ai_recommendations.txt', 'w') as f:
            f.write(recommendations)
        
        st.success("✅ Fresh insights generated!")
        st.info(recommendations)
else:
    # Show saved recommendations by default
    with open('ai_recommendations.txt', 'r') as f:
        st.info(f.read())

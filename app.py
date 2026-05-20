import os
import pandas as pd
import streamlit as st

df = pd.read_csv('marketing_campaign.csv', sep=';')
df['Income'] = df['Income'].fillna(df['Income'].median())
df['TotalSpend'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
df['TotalPurchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases']
df['TotalCampaignsAccepted'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5']
df['Age'] = 2025 - df['Year_Birth']
df['AgeGroup'] = pd.cut(df['Age'], bins=[18,30,40,50,60,70,100], labels=['18-30','31-40','41-50','51-60','61-70','70+'])
df['R_Score'] = pd.qcut(df['Recency'], q=5, labels=[5,4,3,2,1]).astype(int)
df['F_Score'] = pd.qcut(df['TotalPurchases'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
df['M_Score'] = pd.qcut(df['TotalSpend'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
def segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif f >= 4 and m >= 4:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2:
        return 'New Customers'
    elif r <= 2 and m >= 4:
        return 'At Risk'
    elif r <= 2 and f >= 4 and m >= 4:
        return 'Cannot Lose Them'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Lost'
    else:
        return 'Potential'

df['Segment'] = df.apply(segment, axis=1)

st.set_page_config(page_title="NovaStyle Marketing Intelligence", layout="wide")
st.title("NovaStyle Marketing Intelligence System")
st.markdown("*AI-powered marketing analytics dashboard*")
st.divider()

tab1, tab2, tab3 = st.tabs(["Overview", "Customer Segments", "AI Insights"])
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{len(df):,}")
    col2.metric("Avg Customer Spend", f"${df['TotalSpend'].mean():.0f}")
    col3.metric("Avg Income", f"${df['Income'].mean():.0f}")
    col4.metric("Campaign Response Rate", f"{df['Response'].mean()*100:.1f}%")
with tab2:
    st.subheader("Customer Segmentation — RFM Analysis")
    st.markdown("*Customers scored on Recency, Frequency, and Monetary value.*")
    st.divider()
    seg_counts = df['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    st.bar_chart(seg_counts.set_index('Segment'))
    st.divider()
    st.subheader("Segment Details and Recommended Actions")
    actions = {
        'Champions': 'Offer VIP early access and referral programs',
        'Loyal Customers': 'Reward with loyalty perks and exclusive offers',
        'New Customers': 'Send onboarding flow and second-purchase incentive',
        'Potential': 'Nurture with personalized content and targeted campaigns',
        'At Risk': 'Launch win-back email sequence immediately',
        'Cannot Lose Them': 'High priority — personal outreach and strong incentive',
        'Lost': 'Sunset or aggressive re-engagement campaign'
    }
    seg_summary = df.groupby('Segment').agg(
        Customers=('ID', 'count'),
        Avg_Spend=('TotalSpend', 'mean'),
        Avg_Recency=('Recency', 'mean'),
        Avg_Purchases=('TotalPurchases', 'mean')
    ).round(1).reset_index()
    seg_summary['Recommended Action'] = seg_summary['Segment'].map(actions)
    seg_summary = seg_summary.sort_values('Customers', ascending=False)
    seg_summary.columns = ['Segment', 'Customers', 'Avg Spend ($)', 'Avg Recency (days)', 'Avg Purchases', 'Recommended Action']
    st.dataframe(seg_summary, use_container_width=True, hide_index=True)
with tab3:
    st.subheader("AI Strategic Recommendations")
    st.markdown("*Generated automatically from live campaign and customer data*")
    if st.button("Generate Fresh AI Insights"):
        from openai import OpenAI
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
        Customer Segments: {df['Segment'].value_counts().to_string()}
        """
        with st.spinner("Analyzing data..."):
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": f"You are a senior marketing analyst. Analyze this data including RFM segments and give 5 executive recommendations:\n{summary}"}]
            )
            recommendations = response.choices[0].message.content
            with open('ai_recommendations.txt', 'w') as f:
                f.write(recommendations)
            st.success("Fresh insights generated!")
            st.info(recommendations)
    else:
        try:
            with open('ai_recommendations.txt', 'r') as f:
                st.info(f.read())
        except:
            st.warning("No recommendations yet. Click the button above to generate!")

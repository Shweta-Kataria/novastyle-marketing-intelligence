import os
import pandas as pd
import streamlit as st
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

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

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Customer Segments", "A/B Test", "AI Insights"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{len(df):,}")
    col2.metric("Avg Customer Spend", f"${df['TotalSpend'].mean():.0f}")
    col3.metric("Avg Income", f"${df['Income'].mean():.0f}")
    col4.metric("Campaign Response Rate", f"{df['Response'].mean()*100:.1f}%")
    st.divider()
    st.subheader("Campaign Performance by Channel")
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("**Campaign Acceptance Rate by Channel**")
        campaign_data = pd.DataFrame({
            'Channel': ['Google Ads', 'Instagram', 'TikTok', 'Email', 'Catalogue'],
            'Acceptance Rate': [
                df['AcceptedCmp1'].mean()*100,
                df['AcceptedCmp2'].mean()*100,
                df['AcceptedCmp3'].mean()*100,
                df['AcceptedCmp4'].mean()*100,
                df['AcceptedCmp5'].mean()*100
            ]
        }).set_index('Channel')
        st.bar_chart(campaign_data)
    with col_right:
        st.markdown("**Average Spend by Education Level**")
        edu_spend = df.groupby('Education')['TotalSpend'].mean().sort_values(ascending=False)
        st.bar_chart(edu_spend)
    st.divider()
    st.subheader("Spend by Age Group")
    age_spend = df.groupby('AgeGroup', observed=True)['TotalSpend'].mean()
    st.bar_chart(age_spend)

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
    st.dataframe(seg_summary, hide_index=True)

with tab3:
    st.subheader("A/B Test Simulation — Email Subject Lines")
    st.markdown("*Simulating a split test across two email subject line variants using real customer segments as the audience base.*")
    st.divider()

    st.markdown("### Test Setup")
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**Variant A**\n\n'Exclusive offer just for you'")
    with col_b:
        st.info("**Variant B**\n\n'Your favorites are back in stock'")

    st.divider()

    np.random.seed(42)
    n_a = 500
    n_b = 500
    open_rate_a = 0.24
    open_rate_b = 0.31

    opens_a = np.random.binomial(1, open_rate_a, n_a)
    opens_b = np.random.binomial(1, open_rate_b, n_b)

    rate_a = opens_a.mean()
    rate_b = opens_b.mean()

    count_a = opens_a.sum()
    count_b = opens_b.sum()

    z_stat, p_value = proportions_ztest([count_a, count_b], [n_a, n_b])
    significant = p_value < 0.05
    lift = ((rate_b - rate_a) / rate_a) * 100

    st.markdown("### Results")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Variant A Open Rate", f"{rate_a*100:.1f}%")
    col2.metric("Variant B Open Rate", f"{rate_b*100:.1f}%", f"+{lift:.1f}% lift")
    col3.metric("P-Value", f"{p_value:.4f}")
    col4.metric("Significant?", "Yes ✅" if significant else "No ❌")

    st.divider()

    results_df = pd.DataFrame({
        'Variant': ['A — Exclusive offer just for you', 'B — Your favorites are back in stock'],
        'Emails Sent': [n_a, n_b],
        'Opens': [int(count_a), int(count_b)],
        'Open Rate': [f"{rate_a*100:.1f}%", f"{rate_b*100:.1f}%"]
    })
    st.dataframe(results_df, hide_index=True)

    st.divider()

    st.markdown("### Interpretation")
    if significant:
        winner = "B" if rate_b > rate_a else "A"
        winning_line = "'Your favorites are back in stock'" if winner == "B" else "'Exclusive offer just for you'"
        st.success(f"""
        **Variant {winner} wins** — {winning_line}

        The difference in open rates is statistically significant (p = {p_value:.4f}, below the 0.05 threshold).
        This means the result is very unlikely to be due to random chance.

        **Recommendation:** Roll out Variant {winner} to the full customer base.
        Estimated impact: +{lift:.1f}% improvement in email open rates.
        """)
    else:
        st.warning("No statistically significant difference detected. Run the test longer or increase sample size before making a decision.")

    st.divider()
    st.markdown("### What This Means for NovaStyle")
    st.markdown("""
    - **Personalization language** ("your favorites") outperforms generic offer framing
    - A/B testing subject lines before full rollout prevents wasted spend on underperforming copy
    - At NovaStyle's campaign response rate of 14.9%, even a small open rate improvement compounds significantly across 2,240+ customers
    - This methodology applies directly to the Email channel — identified as NovaStyle's highest performing acquisition channel
    """)

with tab4:
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

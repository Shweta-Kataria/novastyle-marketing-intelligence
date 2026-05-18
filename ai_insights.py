import os
import pandas as pd
from openai import OpenAI

# Load and prepare data
df = pd.read_csv('marketing_campaign.csv', sep=';')
df['Income'] = df['Income'].fillna(df['Income'].median())
df['TotalSpend'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
df['TotalCampaignsAccepted'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5']

# Build data summary
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
"""

# Connect to OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": f"You are a senior marketing analyst. Analyze this data and give 5 executive recommendations:\n{summary}"
    }]
)

print(response.choices[0].message.content)

# Save recommendations to a file
with open('ai_recommendations.txt', 'w') as f:
    f.write(response.choices[0].message.content)

print("Recommendations saved to ai_recommendations.txt!")

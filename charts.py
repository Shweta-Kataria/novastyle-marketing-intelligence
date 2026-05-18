import pandas as pd
import matplotlib.pyplot as plt

# Load and clean data
df = pd.read_csv('marketing_campaign.csv', sep=';')
df['Income'] = df['Income'].fillna(df['Income'].median())

# Create KPIs
df['TotalSpend'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
df['TotalPurchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases']
df['TotalCampaignsAccepted'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5']
df['Age'] = 2025 - df['Year_Birth']
df['EngagementScore'] = df['TotalSpend'] + (df['TotalPurchases'] * 10) + (df['TotalCampaignsAccepted'] * 20)

# Chart 1 — Average Spend by Education
plt.figure()
df.groupby('Education')['TotalSpend'].mean().plot(kind='bar', color='steelblue')
plt.title('Average Customer Spend by Education Level')
plt.xlabel('Education')
plt.ylabel('Average Spend ($)')
plt.tight_layout()
plt.savefig('chart_spend_by_education.png')
plt.close()
print("Chart 1 saved!")

# Create age groups
df['AgeGroup'] = pd.cut(df['Age'], bins=[18, 30, 40, 50, 60, 70, 100], labels=['18-30', '31-40', '41-50', '51-60', '61-70', '70+'])

# Chart 2 — Average Spend by Age Group
plt.figure()
df.groupby('AgeGroup', observed=True)['TotalSpend'].mean().plot(kind='bar', color='coral')
plt.title('Average Customer Spend by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Spend ($)')
plt.tight_layout()
plt.savefig('chart_spend_by_age.png')
plt.close()
print("Chart 2 saved!")

# Chart 3 — Campaign Acceptance Rate
plt.figure()
campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5']
campaign_labels = ['Google Ads', 'Instagram', 'TikTok', 'Email', 'Catalogue']
campaign_rates = [df[col].mean() * 100 for col in campaign_cols]

plt.bar(campaign_labels, campaign_rates, color='mediumpurple')
plt.title('Campaign Acceptance Rate by Channel (%)')
plt.xlabel('Channel')
plt.ylabel('Acceptance Rate (%)')
plt.tight_layout()
plt.savefig('chart_campaign_performance.png')
plt.close()
print("Chart 3 saved!")

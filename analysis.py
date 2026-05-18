import pandas as pd
df = pd.read_csv('marketing_campaign.csv', sep=';')
print(df.head())
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

print("Missing values:")
print(df.isnull().sum())

print("Duplicates:", df.duplicated().sum())

df['Income'] = df['Income'].fillna(df['Income'].median())

print("Missing values after fix:", df.isnull().sum().sum())

# Total spending per customer
df['TotalSpend'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']

# Total purchases per customer
df['TotalPurchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases']

# Total campaigns accepted
df['TotalCampaignsAccepted'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5']

# Customer Age
df['Age'] = 2026 - df['Year_Birth']

# Engagement Score
df['EngagementScore'] = df['TotalSpend'] + (df['TotalPurchases'] * 10) + (df['TotalCampaignsAccepted'] * 20)

print(df[['TotalSpend', 'TotalPurchases', 'TotalCampaignsAccepted', 'Age', 'EngagementScore']].head())
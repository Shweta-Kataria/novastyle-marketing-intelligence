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

# RFM Scoring
df['R_Score'] = pd.qcut(df['Recency'], q=5, labels=[5,4,3,2,1]).astype(int)
df['F_Score'] = pd.qcut(df['TotalPurchases'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)
df['M_Score'] = pd.qcut(df['TotalSpend'].rank(method='first'), q=5, labels=[1,2,3,4,5]).astype(int)

df['RFM_Score'] = df['R_Score'].astype(str) + df['F_Score'].astype(str) + df['M_Score'].astype(str)

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
        return "Can't Lose Them"
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Lost'
    else:
        return 'Potential'

df['Segment'] = df.apply(segment, axis=1)

print(df['Segment'].value_counts())
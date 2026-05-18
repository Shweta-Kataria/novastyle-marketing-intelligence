import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Load and clean data
df = pd.read_csv('marketing_campaign.csv', sep=';')
df['Income'] = df['Income'].fillna(df['Income'].median())

# Create features
df['TotalSpend'] = df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] + df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds']
df['TotalPurchases'] = df['NumWebPurchases'] + df['NumCatalogPurchases'] + df['NumStorePurchases']
df['TotalCampaignsAccepted'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5']
df['Age'] = 2025 - df['Year_Birth']

# Define what we're predicting
X = df[['Income', 'TotalSpend', 'TotalPurchases', 'TotalCampaignsAccepted', 'Age', 'Recency', 'NumWebVisitsMonth']]
y = df['Response']

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy*100:.1f}%")
print("\nDetailed Report:")
print(classification_report(y_test, y_pred))

import matplotlib.pyplot as plt

# Feature importance
features = ['Income', 'TotalSpend', 'TotalPurchases', 'TotalCampaignsAccepted', 'Age', 'Recency', 'NumWebVisitsMonth']
importances = model.feature_importances_

plt.figure()
plt.barh(features, importances, color='steelblue')
plt.title('What Predicts Campaign Response?')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('chart_feature_importance.png')
plt.close()
print("Feature importance chart saved!")
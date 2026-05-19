# 🛍️ NovaStyle AI Marketing Intelligence System

## Business Problem
NovaStyle, an e-commerce fashion brand, was struggling with:
- Rising ad costs with unclear ROI
- Low campaign acceptance rates
- Poor understanding of customer behavior
- Inefficient budget allocation across channels

## Solution
I built an end-to-end AI-powered marketing intelligence system that:
- Analyzes customer behavior across 5 marketing channels
- Calculates advanced marketing KPIs
- Uses machine learning to predict campaign response
- Generates automated executive recommendations using AI
- Presents everything in an interactive live dashboard
- **Automatically refreshes AI insights when underlying data changes — making it suitable for real-world deployment where data updates continuously**

## Tech Stack
| Area | Tool |
|------|------|
| Data Cleaning | Python + Pandas |
| Visualization | Matplotlib |
| Machine Learning | Scikit-learn |
| AI Insights | OpenAI API |
| Dashboard | Streamlit |

## Key Findings
- Email campaigns had the highest acceptance rate
- Instagram significantly underperformed all other channels
- PhD and Graduate customers spend the most
- Customers aged 60+ are the highest value segment
- Total spend and recency are the strongest predictors of campaign response

## ML Model
- Algorithm: Random Forest Classifier
- Accuracy: 86%
- Target: Predicting customer campaign response
- Top predictive features: Total Spend, Recency, Income

## AI Integration
- Fed campaign and customer data into OpenAI API
- Generated 5 executive-level strategic recommendations automatically
- Recommendations saved and displayed live in the dashboard

## Business Impact
- Identified Instagram as underperforming — recommend reallocating budget
- Identified Email and TikTok as top channels for increased investment
- Built predictive model to target most likely responders saving wasted spend

## How To Run
```bash
pip3 install pandas matplotlib scikit-learn openai streamlit
streamlit run app.py
```

## Project Structure
```
novastyle-project/
├── analysis.py          ← data cleaning & KPIs
├── charts.py            ← visualizations
├── model.py             ← machine learning
├── ai_insights.py       ← OpenAI integration
├── app.py               ← Streamlit dashboard
└── README.md            ← you are here
```
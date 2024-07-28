# RFV Analysis Application

This Streamlit application performs RFV (Recency, Frequency, Value) analysis on a dataset of customer purchases. The app allows users to upload their own dataset, visualize RFV segments, and download the results.

<link src="">URL to the Web App hosting the Application</link>

## Features

- **Data Upload:** Users can upload a CSV file containing their purchase data. The input data must follow the format of the provided `data.csv` file.
- **Recency Calculation:** Computes the recency of each customer's last purchase.
- **Frequency Calculation:** Counts the number of purchases each customer made.
- **Monetary Value Calculation:** Sums the total amount spent by each customer.
- **RFV Score Calculation:** Classifies customers into segments based on their recency, frequency, and monetary value.
- **Marketing Actions:** Recommends specific marketing actions for each RFV segment.
- **Visualizations:** Generates beautiful visualizations including a count plot of RFV segments and a pair plot with specific customer tiers.
- **Downloadable Results:** Allows users to download the RFV analysis results as an Excel file.

## How to Use

1. Upload your `data.csv` file (must follow the same format as the provided `data.csv`, located inside of the input folder of this repository).
2. View the RFV analysis results and visualizations.
3. Download the RFV analysis results as an Excel file.

## Visualizations

- **Count Plot:** Displays the count of each RFV segment, with bars colored in lime green.
- **Pair Plot:** Displays a pair plot with hue on specific customer tiers (e.g., AAA and DDD).

## Example Actions

The application provides the following marketing actions for different RFV segments:

```python
dict_acoes = {
    'AAA': 'Send discount coupons, Ask them to recommend our product to a friend, Send free samples when launching a new product.',
    'DDD': 'Churn! customers who spent very little and made few purchases, do nothing',
    'DAA': 'Churn! customers who spent a lot and made many purchases, send discount coupons to try to recover them',
    'CAA': 'Churn! customers who spent a lot and made many purchases, send discount coupons to try to recover them'
}

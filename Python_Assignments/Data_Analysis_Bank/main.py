# Assignment 
# create 2 bar charts from the bank transactions csv file
# 1) The total amount for both deposits and withdrawals for the whole year
# 2) The total amount for both deposits and withdrawals for each month of the year

import pandas as pd
import matplotlib.pyplot as plt

# Load the data from a CSV file into a pandas DataFrame.
df = pd.read_csv('Data_Analysis_Bank/bank_transactions.csv')

# create a new DataFrame, df_deposits, containing only deposit transactions.
df_deposits = df[df["Transaction Type"] == "Deposit"]

# create a new DataFrame, df_withdrawals, containing only withdrawal transactions.
df_withdrawals = df[df["Transaction Type"] == "Withdrawal"]

# Calculate the total sum of the "Amount" column in the df_deposits DataFrame.
deposits_total = df_deposits.Amount.sum()

# Similarly, calculate the total sum of the "Amount" column in the df_withdrawals DataFrame.
withdrawals_total = df_withdrawals.Amount.sum()


# Create a DataFrame for the totals
totals = pd.DataFrame({
    'Transaction Type': ['Deposit', 'Withdrawal'],
    'Total Amount': [deposits_total, withdrawals_total]
})

# Plot the bar chart
plt.figure(figsize=(10,6))
plt.bar(totals['Transaction Type'], totals['Total Amount'], color=['green', 'red'])
plt.title('Total Amounts for Deposits and Withdrawals')
plt.xlabel('Transaction Type')
plt.ylabel('Total Amount')
# Set y-axis scale in 1000s
plt.yticks(ticks=range(0, int(max(totals['Total Amount']))+1000, 1000))
plt.show()

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Create a new column 'Month' to hold the month extracted from 'Date'
df['Month'] = df['Date'].dt.month_name()

# Define the correct order for the months as month_name() will order alphabetically otherwise.
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Convert 'Month' to a category variable with the correct order
df['Month'] = pd.Categorical(df['Month'], categories=month_order, ordered=True)

# Group the data by month and transaction type, then sum the amounts
grouped = df.groupby(['Month', 'Transaction Type'])['Amount'].sum().unstack()

# Plotting
grouped.plot(kind='bar', figsize=(12, 8))

plt.title('Monthly Deposits and Withdrawals')
plt.xlabel('Month')
plt.ylabel('Total Amount')
plt.xticks(rotation='horizontal')
plt.show()



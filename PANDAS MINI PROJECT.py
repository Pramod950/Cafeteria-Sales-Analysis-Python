import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sales_data = pd.read_csv("D:/DATA ANALYTICS/PYTHON/MINI PROJECT/Cafe_Sales.csv")
#print(sales_data)
#print(sales_data.info())
#print(sales_data.describe())
#print(sales_data.to_string())

#DATA ANALYSIS
#Data Cleaning
sales_data.replace((" ","UNKNOWN","ERROR"),np.nan,inplace=True)

#Changing data types
sales_data["Transaction Date"]=pd.to_datetime(sales_data["Transaction Date"],errors="coerce")
sales_data["Quantity"]=sales_data["Quantity"].astype('Int64')
sales_data[["Price Per Unit ($)","Total Spent ($)"]]=sales_data[["Price Per Unit ($)","Total Spent ($)"]].apply(pd.to_numeric,errors="coerce")

#Filling missing values

p_nulls = None

while True:
    c_nulls = (sales_data["Item"].isna().sum()+sales_data["Quantity"].isna().sum()+sales_data["Price Per Unit ($)"].isna().sum()+
               sales_data["Total Spent ($)"].isna().sum())
    if c_nulls == p_nulls:
        break
    p_nulls = c_nulls
    
    mode_item = sales_data.groupby("Price Per Unit ($)")["Item"].agg(lambda x: x.mode()[0])
    sales_data["Item"]= sales_data["Item"].fillna(sales_data["Price Per Unit ($)"].map(mode_item))
    
    item_price_map = sales_data.groupby("Item")["Price Per Unit ($)"].agg(lambda x: x.mode()[0])
    sales_data["Price Per Unit ($)"] = sales_data["Price Per Unit ($)"].fillna(sales_data["Item"].map(item_price_map))

    sales_data["Quantity"] = sales_data["Quantity"].fillna(sales_data["Total Spent ($)"] // sales_data["Price Per Unit ($)"]).astype('Int64')

    sales_data["Price Per Unit ($)"] = sales_data["Price Per Unit ($)"].fillna(sales_data["Total Spent ($)"]/sales_data["Quantity"])

    sales_data["Total Spent ($)"] = sales_data["Total Spent ($)"].fillna(sales_data["Quantity"]*sales_data["Price Per Unit ($)"])

#Removing the data that cannot be filled and that won't help in analysis
counts = sales_data[["Quantity", "Price Per Unit ($)", "Total Spent ($)"]].notna().sum(axis=1)
sales_data = sales_data[counts != 1]

sales_data[["Payment Method","Location","Transaction Date"]]=sales_data[["Payment Method","Location","Transaction Date"]].fillna("Unknown")
#Removing Duplicates
#print(sales_data.duplicated().to_string())
sales_data = sales_data.drop_duplicates()

#Sorting
sales_data["Transaction Date"]=pd.to_datetime(sales_data["Transaction Date"],errors="coerce")
sales_data = sales_data.sort_values(by="Transaction Date")

#Exporting the excel
#sales_data.to_csv("D:/DA & DS/PYTHON/MINI PROJECT/Cafe_sales_cleandata.csv",index=False)

#finding unique values
#print(sales_data["Transaction Date"].nunique())

#Finding correlations
num_data = sales_data.select_dtypes(include='number')
corr = num_data.corr()
#print(corr)

#Heat map
#sns.heatmap(corr)
#plt.show()

#scatter plot
#sales_data.plot(kind="scatter",x="Price Per Unit ($)",y="Total Spent ($)")
sales_data.plot(kind="scatter",x="Quantity",y="Total Spent ($)")
#plt.show()

#Bar Chart
item_sales=sales_data.groupby("Item")["Price Per Unit ($)"].sum().sort_values()
item_sales.plot(kind="bar")
#plt.show()

#Line chart
sales_data=sales_data.set_index("Transaction Date", drop=False)
monthly=sales_data["Total Spent ($)"].resample("M").sum()
monthly.plot(kind="line")
#plt.ylim(6500, 7500)
#plt.show()

#Histogram
plt.hist(sales_data["Total Spent ($)"], bins=10)
plt.xlabel("Total Spent ($)")
plt.ylabel("Frequency")
#plt.show()

#Box Plot
plt.boxplot(sales_data["Total Spent ($)"])
#plt.show()







#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

# Load and parse dates
df = pd.read_csv(r'C:\Users\Admin\Downloads\sales_data_2023.csv', parse_dates=['Date'])

# Fill missing values
df.fillna(0, inplace=True)

# Monthly aggregation
df['Month'] = df['Date'].dt.to_period('M').astype(str)
monthly_sales = df.groupby('Month')['Revenue'].sum().reset_index()


# In[4]:


import os
import matplotlib.pyplot as plt
import seaborn as sns

# Create folder
os.makedirs("images", exist_ok=True)

# Plot the sales trend
plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly_sales, x='Month', y='Revenue', marker='o')
plt.xticks(rotation=45)
plt.title('Monthly Revenue Trend')
plt.tight_layout()

# Save plot
plt.savefig('images/line_trend.png')
plt.show()


# In[5]:


# Lag feature
monthly_sales['Revenue_Lag1'] = monthly_sales['Revenue'].shift(1)
monthly_sales.dropna(inplace=True)


# In[6]:


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

X = monthly_sales[['Revenue_Lag1']]
y = monthly_sales['Revenue']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluation
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
print(f"RMSE: {rmse}, MAE: {mae}")


# In[7]:


import numpy as np

plt.figure(figsize=(10,5))
plt.plot(y_test.index, y_test.values, label='Actual')
plt.plot(y_test.index, y_pred, label='Predicted')
plt.legend()
plt.title('Actual vs Predicted Sales')
plt.savefig('images/forecast_graph.png')
plt.show()


# In[ ]:





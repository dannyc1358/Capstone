import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm

#Load original dataset for cleaning
df = pd.read_csv('2024_brooklyn.csv')
pd.set_option('display.max_columns', None)
print(df.head())
print(df.shape)

#Replacing spaces/newlines/tabs with underscore
df.columns = df.columns.str.replace(r'\s+', '_', regex=True)
print(df.columns)

#Calculate essential columns
df['SALE_DATE'] = pd.to_datetime(df['SALE_DATE'], format='%m/%d/%y', errors='coerce')
df['BUILDING_AGE'] = df['SALE_DATE'].dt.year - df['YEAR_BUILT']
print(df.head())

#Removing unnecessary columns
df = df[['RESIDENTIAL_UNITS', 'GROSS_SQUARE_FEET', 'TAX_CLASS_AT_TIME_OF_SALE', 'BUILDING_CLASS_AT_TIME_OF_SALE', 'SALE_PRICE', 'BUILDING_AGE']]
print(df.head())

#Convert strings to numeric
numeric_cols = ['RESIDENTIAL_UNITS', 'GROSS_SQUARE_FEET', 'SALE_PRICE', 'BUILDING_AGE']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
print(df.head())

#Drop rows with missing value
essential_cols = ['RESIDENTIAL_UNITS', 'GROSS_SQUARE_FEET', 'SALE_PRICE', 'BUILDING_AGE']
df = df.dropna(subset=essential_cols)

#Drop rows with 0 values
df = df[(df[essential_cols] != 0).all(axis=1)]
print(df.head())

#Drop rows with sale price less than 200000
df = df[df['SALE_PRICE'] >= 200000].reset_index(drop=True)

#Filter data for residential property only
tax_filter = df['TAX_CLASS_AT_TIME_OF_SALE'].isin([1, 2])

class_filter = (
        df['BUILDING_CLASS_AT_TIME_OF_SALE'].str[0].isin(['A', 'B']) |
        ((df['BUILDING_CLASS_AT_TIME_OF_SALE'].str[0] == 'C') &
         (~df['BUILDING_CLASS_AT_TIME_OF_SALE'].str.startswith('CM')))
)
df_residential = df[tax_filter & class_filter].reset_index(drop=True)
print(df_residential.head())
print(df_residential.shape)

df_residential = df_residential.drop(columns=['BUILDING_CLASS_AT_TIME_OF_SALE', 'TAX_CLASS_AT_TIME_OF_SALE'])

df_residential.info()
df_residential.describe()

#Save cleaned dataset
df_residential.to_csv('residential.csv', index=False)

#Exploratory data analysis
    #visualizations of features vs sale price
plt.scatter(df_residential['RESIDENTIAL_UNITS'], df_residential['SALE_PRICE'])
plt.xlabel('Residential Units')
plt.ylabel('Sale Price')
plt.title('Residential vs. Sale Price')
plt.tight_layout()
plt.show()

plt.scatter(df_residential['BUILDING_AGE'], df_residential['SALE_PRICE'])
plt.xlabel('Building Age')
plt.ylabel('Sale Price')
plt.title('Building Age vs. Sale Price')
plt.tight_layout()
plt.show()

plt.scatter(df_residential['GROSS_SQUARE_FEET'], df_residential['SALE_PRICE'])
plt.xlabel('Gross Square Feet')
plt.ylabel('Sale Price')
plt.title('Gross Square Feet vs. Sale Price')
plt.tight_layout()
plt.show()

#Handling skewness
df_residential['LOG_SALE_PRICE'] = np.log(df_residential['SALE_PRICE'])

#Defining features and target variables
X = df_residential[['RESIDENTIAL_UNITS', 'GROSS_SQUARE_FEET', 'BUILDING_AGE']]
y = df_residential['LOG_SALE_PRICE']

#Split dataset into training, validation, and testing into 70/15/15
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)

X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

X_train.to_csv('X_train.csv', index=False)
X_val.to_csv('X_val.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_val.to_csv('y_val.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

#Train regression model
model = LinearRegression()
model.fit(X_train, y_train)

#Validate metrics for performance
val_pred = model.predict(X_val)
val_mse = mean_squared_error(y_val, val_pred)
val_rmse = np.sqrt(val_mse)
print('Validation RMSE:', val_rmse)

#Test metrics for performance
test_pred = model.predict(X_test)
test_mse = mean_squared_error(y_test, test_pred)
test_rmse = np.sqrt(test_mse)
print('Test RMSE:', test_rmse)

#regression summary table
X_train_const = sm.add_constant(X_train)
model_sm = sm.OLS(y_train, X_train_const).fit()
print(model_sm.summary())

#predicted listing price & percent change
predicted_price = np.exp(test_pred)
pct_change = (np.exp(model_sm.params.drop('const')) - 1) * 100
print('Pct change:', pct_change)

#finding optimal sale price with a dynamic margin based on features
df_residential['PREDICTED_PRICE'] = np.exp(model.predict(X))
df_residential['MARGIN'] = (
        0.04 #base margin
        + 0.02 * (df_residential['BUILDING_AGE'] < 25) #buildings built within 25 years from sale year
        + 0.01 * (df_residential['GROSS_SQUARE_FEET'] > 1100) #buildings greater than 1100 sq ft
        + 0.01 * (df_residential['GROSS_SQUARE_FEET'] > 2000) # buildings greater than 2000 sq ft
)
df_residential['OPTIMAL_LIST_PRICE'] = (
        df_residential['PREDICTED_PRICE'] * (1 + df_residential['MARGIN'])
)

df_residential['PREDICTED_PRICE'] = df_residential['PREDICTED_PRICE'].round(0)
df_residential['OPTIMAL_LIST_PRICE'] = df_residential['OPTIMAL_LIST_PRICE'].round(0)
print(df_residential.head())

df_residential.to_csv('optimal_price.csv', index=False)

#visualizations to compare predicted price and optimal list price to actual sale price
sns.set_style('darkgrid')
sample = df_residential.sample(min(1000, len(df_residential)), random_state=42)

plt.figure(figsize=(12, 8))
plt.scatter(sample['SALE_PRICE'], sample['PREDICTED_PRICE'], color='blue', alpha=0.3, label='Predicted Price')
plt.scatter(sample['SALE_PRICE'], sample['OPTIMAL_LIST_PRICE'], color='orange', alpha=0.3, label='Optimal List Price')
max_price = max(sample[['SALE_PRICE', 'PREDICTED_PRICE', 'OPTIMAL_LIST_PRICE']].max())

plt.plot([0, max_price], [0, max_price], color='red', linestyle='--', label='Perfect Price')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Sale Price ($)')
plt.ylabel('Predicted Price/Optimal List Price ($)')
plt.title('Predicted Price vs. Optimal List Price vs. Sale Price')
plt.legend()
plt.tight_layout()
plt.show()
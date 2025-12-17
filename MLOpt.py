import pandas as pd

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
df = df[['RESIDENTIAL_UNITS', 'LAND_SQUARE_FEET', 'GROSS_SQUARE_FEET', 'TAX_CLASS_AT_TIME_OF_SALE', 'BUILDING_CLASS_AT_TIME_OF_SALE', 'SALE_PRICE', 'BUILDING_AGE']]
print(df.head())

#Convert strings to numeric
numeric_cols = ['RESIDENTIAL_UNITS', 'LAND_SQUARE_FEET', 'GROSS_SQUARE_FEET', 'SALE_PRICE', 'BUILDING_AGE']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
print(df.head())

#Drop rows with missing value
essential_cols = ['RESIDENTIAL_UNITS', 'LAND_SQUARE_FEET', 'GROSS_SQUARE_FEET', 'SALE_PRICE', 'BUILDING_AGE']
df = df.dropna(subset=essential_cols)

#Drop rows with 0 values
df = df[(df[essential_cols] != 0).all(axis=1)]
print(df.head())

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

#Save cleaned dataset
df_residential.to_csv('residential.csv', index=False)
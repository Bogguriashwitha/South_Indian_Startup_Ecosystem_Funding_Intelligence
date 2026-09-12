import pandas as pd

# Load the Excel dataset
df = pd.read_csv("data/startup_funding.csv")

# Dataset size
print("Dataset Shape:")
print(df.shape)

# Column names
print("\nColumn Names:")
print(df.columns.tolist())

# First 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Data types
print("\nData Types:")
print(df.dtypes)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())
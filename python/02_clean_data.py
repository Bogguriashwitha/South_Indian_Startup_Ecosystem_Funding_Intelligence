import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("data/startup_funding.csv")

print("Original dataset shape:")
print(df.shape)

# -----------------------------------------
# 1. Clean column names
# -----------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nCleaned column names:")
print(df.columns.tolist())

# -----------------------------------------
# 2. Remove completely empty rows
# -----------------------------------------

df = df.dropna(how="all")

# -----------------------------------------
# 3. Remove duplicate records
# -----------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate records:", duplicates)

df = df.drop_duplicates()

# -----------------------------------------
# 4. Clean date
# -----------------------------------------

df["date_dd/mm/yyyy"] = pd.to_datetime(
    df["date_dd/mm/yyyy"],
    dayfirst=True,
    errors="coerce"
)

# Create year column
df["year"] = df["date_dd/mm/yyyy"].dt.year

# -----------------------------------------
# 5. Clean text columns
# -----------------------------------------

text_columns = [
    "startup_name",
    "industry_vertical",
    "subvertical",
    "city__location",
    "investors_name",
    "investmentntype"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# -----------------------------------------
# 6. Handle missing City
# -----------------------------------------

df["city__location"] = df["city__location"].fillna("Unknown")
# Standardize city names
city_mapping = {
    "Bangalore": "Bengaluru",
    "Bengaluru": "Bengaluru"
}

df["city__location"] = df["city__location"].replace(city_mapping)


# Standardize industry vertical names
industry_mapping = {
    "eCommerce": "E-Commerce",
    "ECommerce": "E-Commerce",
    "E-commerce": "E-Commerce",
    "Ecommerce": "E-Commerce",
    "Ed-Tech": "Education",
    "EdTech": "Education",
    "Online Education Platform": "Education",
    "FinTech": "Finance",
    "Fin-Tech": "Finance",
    "Food and Beverage": "Food & Beverage",
    "Transport": "Transportation",
    "Information Technology": "Technology",
    "IT": "Technology"
}

df["industry_vertical"] = df["industry_vertical"].replace(industry_mapping)


# Create broader sector categories
def categorize_sector(sector):
    sector = str(sector).lower()

    if sector == "unknown":
        return "Unknown"
    elif "ecommerce" in sector or "e-commerce" in sector:
        return "E-Commerce"
    elif "finance" in sector or "fintech" in sector:
        return "Finance"
    elif "health" in sector or "healthcare" in sector:
        return "Healthcare"
    elif "education" in sector or "edtech" in sector:
        return "Education"
    elif "logistic" in sector:
        return "Logistics"
    elif "food" in sector:
        return "Food & Beverage"
    elif "transport" in sector or "mobility" in sector:
        return "Transportation"
    elif "real estate" in sector or "property" in sector:
        return "Real Estate"
    elif "technology" in sector or "software" in sector or "saas" in sector or "tech" in sector:
        return "Technology"
    elif "automobile" in sector or "automotive" in sector:
        return "Automobile"
    elif "travel" in sector or "tourism" in sector:
        return "Travel"
    else:
        return "Other"


df["sector_category"] = df["industry_vertical"].apply(categorize_sector)

# -----------------------------------------
# 7. Handle missing Industry Vertical
# -----------------------------------------

df["industry_vertical"] = df["industry_vertical"].fillna("Unknown")

# -----------------------------------------
# 8. Clean funding amount
# -----------------------------------------

df["amount_in_usd"] = (
    df["amount_in_usd"]
    .astype("string")
    .str.replace(",", "", regex=False)
    .str.replace("$", "", regex=False)
    .str.strip()
)

df["amount_in_usd"] = pd.to_numeric(
    df["amount_in_usd"],
    errors="coerce"
)

# -----------------------------------------
# 9. Check negative funding
# -----------------------------------------

negative_funding = (df["amount_in_usd"] < 0).sum()

print("\nNegative funding records:", negative_funding)

# -----------------------------------------
# 10. City standardization
# -----------------------------------------

# Standardize industry vertical names
industry_mapping = {
    "eCommerce": "E-Commerce",
    "ECommerce": "E-Commerce",
    "E-commerce": "E-Commerce",
    "Ecommerce": "E-Commerce",
    "E-Commerce": "E-Commerce",

    "Ed-Tech": "Education",
    "EdTech": "Education",
    "Online Education Platform": "Education",

    "FinTech": "Finance",
    "Fin-Tech": "Finance",

    "Food and Beverage": "Food & Beverage",

    "Transport": "Transportation",

    "Information Technology": "Technology",
    "IT": "Technology"
}

df["industry_vertical"] = df["industry_vertical"].replace(industry_mapping)

# -----------------------------------------
# 11. Final dataset information
# -----------------------------------------

print("\nFinal dataset shape:")
print(df.shape)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

print("\nYears covered:")
print(df["year"].min(), "to", df["year"].max())

print("\nCities:")
print(df["city__location"].nunique())

print("\nIndustry verticals:")
print(df["industry_vertical"].nunique())

# -----------------------------------------
# 12. Save cleaned dataset
# -----------------------------------------

df.to_csv(
    "data/startup_clean.csv",
    index=False
)

print("\nCleaned dataset saved as:")
print("data/startup_clean.csv")
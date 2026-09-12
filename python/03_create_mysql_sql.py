import pandas as pd

# Read cleaned CSV
df = pd.read_csv("data/startup_clean.csv")

# SQL file location
output_file = "sql/startup_funding_insert.sql"

# Create SQL statements
with open(output_file, "w", encoding="utf-8") as f:

    for _, row in df.iterrows():

        values = []

        for value in row:
            if pd.isna(value):
                values.append("NULL")
            elif isinstance(value, (int, float)):
                values.append(str(value))
            else:
                value = str(value).replace("'", "''")
                values.append(f"'{value}'")

        sql = f"INSERT INTO startup_funding_final VALUES ({', '.join(values)});\n"
        f.write(sql)

print("SQL file created successfully!")
print("Total records:", len(df))
print("Output:", output_file)
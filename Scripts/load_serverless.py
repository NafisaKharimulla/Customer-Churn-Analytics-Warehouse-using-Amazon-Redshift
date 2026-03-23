import boto3
import pandas as pd
import time

# ---------- CONFIG ----------
REGION = "ap-south-1"
WORKGROUP_NAME = "telecom-workgroup"
DATABASE_NAME = "dev"
TABLE_NAME = "customer_churn"
CSV_FILE = "telecom_customer_churn.csv"
# ----------------------------

# Initialize Redshift Data API client
client = boto3.client("redshift-data", region_name=REGION)

# Load CSV into Pandas
df = pd.read_csv(CSV_FILE)

# Insert each row into Redshift
for idx, row in df.iterrows():
    # Prepare INSERT statement
    insert_sql = f"""
    INSERT INTO {TABLE_NAME} (customer_id, gender, age, married, num_dependents, city, zip_code, latitude, longitude, num_referrals)
    VALUES (
        '{row['Customer ID']}', 
        '{row['Gender']}', 
        '{row['Age']}', 
        '{row['Married']}', 
        '{row['Number of Dependents']}', 
        '{row['City']}', 
        '{row['Zip Code']}', 
        '{row['Latitude']}', 
        '{row['Longitude']}', 
        '{row['Number of Referrals']}'
    )
    """
    # Execute the statement
    response = client.execute_statement(
        WorkgroupName=WORKGROUP_NAME,
        Database=DATABASE_NAME,
        Sql=insert_sql
    )
    
    # Print progress
    print(f"Inserted row {idx+1} / {len(df)}")

    # Optional: wait a tiny bit to avoid throttling
    time.sleep(0.05)

print("All rows inserted successfully!")

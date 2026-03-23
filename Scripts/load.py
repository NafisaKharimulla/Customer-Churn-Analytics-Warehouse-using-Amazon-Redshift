import boto3
import pandas as pd

# ------------------------------
# CONFIGURATION
# ------------------------------
REGION = "ap-south-1"
WORKGROUP = "telecom-workgroup"
TABLE_NAME = "customer_churn"
CSV_FILE = "telecom_customer_churn.csv"

# ------------------------------
# INITIALIZE REDSHIFT DATA API CLIENT
# ------------------------------
client = boto3.client('redshift-data', region_name=REGION)

# ------------------------------
# READ CSV IN CHUNKS
# ------------------------------
chunk_size = 100  # number of rows per insert
df_iter = pd.read_csv(CSV_FILE, chunksize=chunk_size)

# ------------------------------
# INSERT EACH CHUNK
# ------------------------------
for idx, chunk in enumerate(df_iter, start=1):
    # Prepare VALUES for SQL
    values_list = []
    for _, row in chunk.iterrows():
        values = [str(x).replace("'", "''") if pd.notnull(x) else 'NULL' for x in row]
        values_str = "(" + ",".join(f"'{v}'" if v != 'NULL' else "NULL" for v in values) + ")"
        values_list.append(values_str)
    
    sql = f"INSERT INTO {TABLE_NAME} VALUES {', '.join(values_list)};"
    
    # Execute insert (without DbUser for serverless)
    response = client.execute_statement(
        WorkgroupName=WORKGROUP,
        Database="dev",
        Sql=sql
    )
    
    print(f"Batch {idx} inserted, Query ID: {response['Id']}")

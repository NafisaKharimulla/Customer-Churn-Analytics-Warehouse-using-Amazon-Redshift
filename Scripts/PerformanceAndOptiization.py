import boto3
import time

# ------------------------------
# Redshift Serverless connection
# ------------------------------
REGION = "ap-south-1"
WORKGROUP_NAME = "telecom-workgroup"  # Your workgroup
DATABASE_NAME = "dev"                 # Your namespace database

client = boto3.client("redshift-data", region_name=REGION)

# ------------------------------
# Function to execute SQL and wait for completion
# ------------------------------
def execute_sql(sql):
    response = client.execute_statement(
        WorkgroupName=WORKGROUP_NAME,
        Database=DATABASE_NAME,
        Sql=sql
    )
    statement_id = response["Id"]
    
    # Poll until finished
    while True:
        desc = client.describe_statement(Id=statement_id)
        status = desc["Status"]
        if status in ["FINISHED", "FAILED", "ABORTED"]:
            break
        time.sleep(1)
    
    if status != "FINISHED":
        print(f"Error executing: {sql}")
        print("Error details:", desc.get("Error", "No error info"))
    else:
        print(f"Successfully executed: {sql}")

# ------------------------------
# Get all tables in the public schema
# ------------------------------
get_tables_sql = """
SELECT tablename
FROM pg_table_def
WHERE schemaname = 'public';
"""

response = client.execute_statement(
    WorkgroupName=WORKGROUP_NAME,
    Database=DATABASE_NAME,
    Sql=get_tables_sql
)

statement_id = response["Id"]
# Wait for the table list to finish
while True:
    desc = client.describe_statement(Id=statement_id)
    status = desc["Status"]
    if status in ["FINISHED", "FAILED", "ABORTED"]:
        break
    time.sleep(1)

if status != "FINISHED":
    print("Failed to fetch table list")
    exit(1)

tables_result = client.get_statement_result(Id=statement_id)
tables = [row[0]["stringValue"] for row in tables_result["Records"]]

print(f"Found tables: {tables}")

# ------------------------------
# Run ANALYZE and VACUUM on each table
# ------------------------------
for table in tables:
    print(f"\nOptimizing table: {table}")
    execute_sql(f"ANALYZE public.{table};")
    execute_sql(f"VACUUM FULL public.{table};")

print("\nRedshift Serverless optimization completed for all tables!")
import boto3
import time

# === AWS Redshift Serverless configuration ===
workgroup_name = "telecom-workgroup"   # Your workgroup name
database_name = "dev"                  # Your database name
region_name = "ap-south-1"             # Your AWS region
db_user = None                          # Leave None for serverless

# === Connect to Redshift Serverless using boto3 ===
client = boto3.client('redshift-data', region_name=region_name)

# === SQL to create analytical table if not exists ===
create_table_sql = """
CREATE TABLE IF NOT EXISTS customer_analytics (
    customer_id VARCHAR(20),
    city VARCHAR(50),
    zip_code VARCHAR(10),
    population INT,
    tenure VARCHAR(10),
    monthly_charges VARCHAR(20),
    total_charges VARCHAR(20),
    customer_status VARCHAR(20)
)
DISTKEY(zip_code)
SORTKEY(customer_id);
"""

# === SQL to insert data from staging tables ===
insert_sql = """
INSERT INTO customer_analytics (customer_id, city, zip_code, population, tenure, monthly_charges, total_charges, customer_status)
SELECT 
    c.customer_id,
    c.city,
    c.zip_code,
    p.population,
    c.tenure,
    c.monthly_charges,
    c.total_charges,
    c.customer_status
FROM customer_churn c
LEFT JOIN telecom_population p
ON c.zip_code = p.zipcode;
"""

def execute_sql(sql_statement):
    response = client.execute_statement(
        WorkgroupName=workgroup_name,
        Database=database_name,
        Sql=sql_statement
    )
    statement_id = response['Id']

    # Wait for execution to complete
    while True:
        desc = client.describe_statement(Id=statement_id)
        status = desc['Status']
        if status in ['FINISHED', 'FAILED', 'ABORTED']:
            break
        print("Executing SQL... please wait")
        time.sleep(2)

    if status == 'FINISHED':
        print("SQL executed successfully!")
    else:
        print(f"SQL execution failed: {desc.get('Error')}")

# === Run the queries ===
print("Creating analytical table...")
execute_sql(create_table_sql)

print("Inserting data into analytical table...")
execute_sql(insert_sql)

print("Task completed! You can now query 'customer_analytics'.")
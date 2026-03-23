import boto3
import csv
import time

# -----------------------------
# Configuration
# -----------------------------
WORKGROUP_NAME = "telecom-workgroup"
DATABASE_NAME = "dev"
# Use the default IAM role or your Redshift credentials
DB_USER = "admin"  

# Initialize Redshift Data API client
client = boto3.client('redshift-data', region_name='ap-south-1')

# -----------------------------
# Queries for Task 7
# -----------------------------
queries = {
    "churn_rate": """
        SELECT 
            ROUND(100.0 * SUM(CASE WHEN customer_status = 'Churned' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_percentage
        FROM customer_analytics;
    """,
    "top_churned_cities": """
        SELECT 
            city,
            COUNT(*) AS churned_customers
        FROM customer_analytics
        WHERE customer_status = 'Churned'
        GROUP BY city
        ORDER BY churned_customers DESC
        LIMIT 10;
    """,
    "churn_by_tenure": """
        SELECT 
            CASE 
                WHEN tenure::INT BETWEEN 0 AND 12 THEN '0-12 months'
                WHEN tenure::INT BETWEEN 13 AND 24 THEN '13-24 months'
                WHEN tenure::INT BETWEEN 25 AND 36 THEN '25-36 months'
                ELSE '36+ months'
            END AS tenure_group,
            COUNT(*) AS churned_customers
        FROM customer_analytics
        WHERE customer_status = 'Churned'
        GROUP BY tenure_group
        ORDER BY tenure_group;
    """,
    "revenue_lost": """
        SELECT 
            SUM(CASE WHEN total_charges IS NOT NULL THEN total_charges::DECIMAL ELSE 0 END) AS total_revenue_lost
        FROM customer_analytics
        WHERE customer_status = 'Churned';
    """,
    "population_vs_customers": """
        SELECT 
            zip_code,
            population,
            COUNT(customer_id) AS customer_count
        FROM customer_analytics
        GROUP BY zip_code, population
        ORDER BY customer_count DESC;
    """
}

# -----------------------------
# Function to run query and save CSV
# -----------------------------
def run_query(query_name, sql):
    print(f"Running query: {query_name} ...")
    response = client.execute_statement(
        WorkgroupName=WORKGROUP_NAME,
        Database=DATABASE_NAME,
        Sql=sql,
        DbUser=DB_USER
    )
    query_id = response['Id']

    # Wait until query finishes
    while True:
        desc = client.describe_statement(Id=query_id)
        status = desc['Status']
        if status in ['FINISHED', 'FAILED', 'ABORTED']:
            break
        time.sleep(1)

    if status != 'FINISHED':
        print(f"Query {query_name} failed with status: {status}")
        return

    result = client.get_statement_result(Id=query_id)
    rows = result['Records']

    # Write CSV
    csv_file = f"{query_name}.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        # Write header
        if rows:
            header = [col['label'] for col in result['ColumnMetadata']]
            writer.writerow(header)
        # Write rows
        for row in rows:
            writer.writerow([list(col.values())[0] if col else None for col in row])
    print(f"Query {query_name} completed. Results saved to {csv_file}")

# -----------------------------
# Execute all queries
# -----------------------------
for name, sql in queries.items():
    run_query(name, sql)

print("All Task 7 queries completed.")
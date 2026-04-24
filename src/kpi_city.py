import sqlite3

def city_kpi(city: str):
    conn = sqlite3.connect('data/db/analytics.db')
    cursor = conn.cursor()
    
    # Use parameterized query to prevent SQL injection
    cursor.execute("""
        SELECT 
            COUNT(*) as total_customers,
            AVG(monthly_spend) as avg_spend,
            SUM(CASE WHEN churned = 1 THEN 1 ELSE 0 END) as churned_count
        FROM customers_raw 
        WHERE city = ?
    """, (city,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        total, avg_spend, churned = result
        print(f"City: {city}")
        print(f"Total Customers: {total}")
        print(f"Average Monthly Spend: ${avg_spend:.2f}")
        print(f"Churned Customers: {churned}")
        print("---")
    else:
        print(f"No data found for city: {city}")
        print("---")

# Test calls
city_kpi("Mumbai")
city_kpi("Mumbai' OR 1=1 --")  # SQL injection attempt
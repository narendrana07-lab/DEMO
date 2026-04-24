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
        return {
            'city': city,
            'total_customers': total,
            'avg_spend': avg_spend,
            'churned_count': churned
        }
    else:
        return None

def test_city_kpi_happy_path():
    result = city_kpi("Mumbai")
    assert result is not None
    assert result['city'] == "Mumbai"
    assert result['total_customers'] == 3  # Based on sample data
    assert result['churned_count'] == 1

def test_city_kpi_injection_attempt():
    result = city_kpi("Mumbai' OR 1=1 --")
    # Should return None or data only for non-existent city, not all rows
    assert result is None or result['total_customers'] == 0
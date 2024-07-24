import mysql.connector

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'stocks'
}

# Sample stock data
stocks = [
    # R1 (Low Risk) Stocks
    ('JNJ', 'Johnson & Johnson', 'R1', 'Healthcare'),
    ('PG', 'Procter & Gamble', 'R1', 'Consumer Goods'),
    ('KO', 'Coca-Cola', 'R1', 'Beverages'),
    ('VZ', 'Verizon', 'R1', 'Telecommunications'),
    ('WMT', 'Walmart', 'R1', 'Retail'),
    ('MCD', "McDonald's", 'R1', 'Restaurants'),
    ('PEP', 'PepsiCo', 'R1', 'Beverages'),
    ('T', 'AT&T', 'R1', 'Telecommunications'),
    ('UL', 'Unilever', 'R1', 'Consumer Goods'),
    ('XOM', 'ExxonMobil', 'R1', 'Oil & Gas'),

    # R2 (Medium Risk) Stocks
    ('AAPL', 'Apple Inc.', 'R2', 'Technology'),
    ('MSFT', 'Microsoft', 'R2', 'Technology'),
    ('GOOGL', 'Alphabet (Google)', 'R2', 'Technology'),
    ('AMZN', 'Amazon', 'R2', 'E-commerce'),
    ('FB', 'Facebook', 'R2', 'Social Media'),
    ('V', 'Visa', 'R2', 'Financial Services'),
    ('JPM', 'JPMorgan Chase', 'R2', 'Banking'),
    ('DIS', 'Disney', 'R2', 'Entertainment'),
    ('NFLX', 'Netflix', 'R2', 'Streaming Services'),
    ('CSCO', 'Cisco Systems', 'R2', 'Networking Technology'),

    # R3 (High Risk) Stocks
    ('TSLA', 'Tesla', 'R3', 'Automotive/Technology'),
    ('NVDA', 'NVIDIA', 'R3', 'Technology'),
    ('AMD', 'Advanced Micro Devices', 'R3', 'Technology'),
    ('COIN', 'Coinbase', 'R3', 'Cryptocurrency'),
    ('SQ', 'Square', 'R3', 'Financial Technology'),
    ('PLTR', 'Palantir Technologies', 'R3', 'Software'),
    ('NIO', 'NIO Inc.', 'R3', 'Automotive'),
    ('BYND', 'Beyond Meat', 'R3', 'Food Products'),
    ('PLUG', 'Plug Power', 'R3', 'Hydrogen Fuel Cells'),
    ('SPCE', 'Virgin Galactic', 'R3', 'Aerospace')
]

# Function to insert stocks into the database
def insert_stocks(stocks):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    for stock in stocks:
        try:
            cursor.execute("""
                INSERT INTO stocks (symbol, name, risk_level, sector)
                VALUES (%s, %s, %s, %s)
            """, stock)
        except mysql.connector.IntegrityError:
            print(f"Stock {stock[0]} already exists. Skipping.")
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    insert_stocks(stocks)
    print("Stock data has been populated in the database.")

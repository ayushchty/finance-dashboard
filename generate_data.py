import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

os.makedirs("data_lake/raw", exist_ok=True)

np.random.seed(42)
n_records = 100_000

data = {
    'timestamp': pd.date_range("2025-01-01", periods=n_records, freq='1min'),
    'user_id': np.random.choice(['user1', 'user2', 'user3'], n_records),
    'symbol': np.random.choice(['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS'], n_records),
    'price': 1000 + np.cumsum(np.random.randn(n_records)) * 10,
    'volume': np.random.randint(100, 10000, n_records),
    'amount': np.random.uniform(100, 5000, n_records),
    'category': np.random.choice(['Food', 'Transport', 'Salary', 'Trade'], n_records)
}

df = pd.DataFrame(data)
df.to_csv("data_lake/raw/1m_transactions.csv", index=False)
print("Created transaction data")

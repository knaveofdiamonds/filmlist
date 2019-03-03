import sys

import pandas as pd

df = pd.read_json(sys.stdin, lines=True)
counts = df.groupby('title').day.count().rename('count')

df = df.set_index('title')
df['count'] = counts
df = df.reset_index()

filtered = df[(df['count'] < 15) & (df['day'].isin(['Sat', 'Sun']) | (df['time'] > '18:30'))]

filtered.sort_values('title').to_csv(sys.stdout, index=False)

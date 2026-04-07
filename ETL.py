import requests
import pandas as pd
import io
response = requests.get('https://www.tourism.jp/wp/wp-content/uploads/2026/03/JTM_inbound_20260304eng.xlsx')
df = pd.read_excel(io.BytesIO(response.content))
df = df.iloc[2:]
df.columns = ["Month", "Visitors", "%Change", "Notes"]
df.drop_index()
print(df)
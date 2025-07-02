import pandas as pd

df = pd.read_csv('data/student_progress.csv')
print("🧾 CSV Columns:", df.columns.tolist())
print(df.head())

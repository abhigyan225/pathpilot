import pandas as pd

df = pd.read_csv("data/students.csv", dtype=str)

# Drop empty or nan student_id
df = df.dropna(subset=["student_id"])
df["student_id"] = df["student_id"].str.strip()
df = df[df["student_id"] != ""]

# Drop exact match for S008
df = df[df["student_id"] != "S008"]

df.to_csv("data/students.csv", index=False)

print("✅ Cleaned and removed S008 if it existed")

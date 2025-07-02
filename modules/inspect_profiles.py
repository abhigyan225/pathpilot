import pandas as pd
import numpy as np

# Load the CSV to match index → student_id
progress_df = pd.read_csv("data/student_progress.csv")

# Load the student profiles (NumPy array)
student_profiles = np.load("models/student_profiles.npy")

# Sanity check
print("📦 Shape of student_profiles:", student_profiles.shape)
print("👥 Number of student IDs in progress_df:", len(progress_df))

# Print mapping index to student_id
print("\n👀 Student index mapping:")
for idx, row in progress_df.iterrows():
    print(f"{idx}: {row['student_id']}")
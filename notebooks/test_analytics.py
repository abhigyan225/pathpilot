import sys
import os
import pandas as pd

# Allow importing from parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.analytics import student_course_completion_rate, most_active_students

# Load student progress
progress_df = pd.read_csv('data/student_progress.csv')

# Run analytics
avg = student_course_completion_rate(progress_df)
print(f"\n📈 Average Courses per Student: {avg:.2f}")

print("\n🏅 Top Active Students:\n")
print(most_active_students(progress_df, top_n=3).to_string(index=False))

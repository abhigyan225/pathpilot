import sys
import os
import pandas as pd

# Allow imports from parent folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.recommender import load_embeddings, recommend_courses_for_student
from modules.course_embedding import load_courses

# Load course data and embeddings
course_df = load_courses("data/courses.csv")
course_embeddings, student_profiles = load_embeddings()

# ✅ Load and transform student progress data
progress_df = pd.read_csv("data/student_progress.csv")
progress_df.columns = progress_df.columns.str.strip().str.lower()  # Normalize column names

# Transform completed_courses column into rows
progress_df = progress_df.assign(
    course_id=progress_df['completed_courses'].str.split(',')
).explode('course_id')

# Clean up spaces
progress_df['course_id'] = progress_df['course_id'].str.strip()

# Set the target student index
student_id = 0

# Recommend courses for that student
recommendations = recommend_courses_for_student(
    student_idx=student_id,
    course_df=course_df,
    course_embeddings=course_embeddings,
    student_profiles=student_profiles,
    top_n=5,
    progress_df=progress_df  # ✅ Fixed: cleaned version
)

# 🖨️ Print recommended courses
print(f"\n📘 Top {len(recommendations)} Recommended Courses for Student {student_id}:\n")
print(recommendations[['course_id', 'title', 'description']].to_string(index=False))



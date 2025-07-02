import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_embeddings(course_path='models/course_embeddings.npy', student_path='models/student_profiles.npy'):
    course_embeddings = np.load(course_path)
    student_profiles = np.load(student_path)
    return course_embeddings, student_profiles

def recommend_courses_for_student(*, student_id, course_df, course_embeddings, student_profiles, top_n, progress_df):
    student_row = progress_df[progress_df['student_id'] == student_id]
    if student_row.empty:
        return pd.DataFrame(columns=['course_id', 'title', 'description'])

    student_idx = student_row.index[0]

    # Check if profile exists
    if student_idx >= len(student_profiles):
        print(f"⚠️ No profile vector for student {student_id}, returning top {top_n} courses.")
        return course_df[['course_id', 'title', 'description']].head(top_n)

    student_vector = student_profiles[student_idx].reshape(1, -1)

    # ✅ Sanitize completed_courses properly
    raw_completed = str(student_row.iloc[0]['completed_courses'])
    completed_ids = [
        c.strip() for c in raw_completed.split(',')
        if c.strip() and c.strip().lower() != "nan"
    ]

    # Filter out completed courses
    mask = ~course_df['course_id'].isin(completed_ids)
    filtered_df = course_df[mask].reset_index(drop=True)
    filtered_embeddings = course_embeddings[mask.to_numpy()]

    if filtered_df.empty:
        return pd.DataFrame(columns=['course_id', 'title', 'description'])

    similarities = cosine_similarity(student_vector, filtered_embeddings)[0]
    top_indices = similarities.argsort()[::-1][:top_n]

    return filtered_df.iloc[top_indices][['course_id', 'title', 'description']]
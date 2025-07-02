import pandas as pd
import numpy as np
import os

def load_student_progress(csv_path):
    df = pd.read_csv(csv_path)
    return df

def build_student_profiles(progress_df, course_df, course_embeddings):
    course_id_to_index = {cid: idx for idx, cid in enumerate(course_df['course_id'])}
    student_vectors = []

    for _, row in progress_df.iterrows():
        completed = str(row['completed_courses']) if pd.notna(row['completed_courses']) else ''
        completed_ids = [c.strip() for c in completed.split(',') if c.strip() and c.strip().lower() != 'nan']

        vectors = []
        for course_id in completed_ids:
            idx = course_id_to_index.get(course_id)
            if idx is not None:
                vectors.append(course_embeddings[idx])

        if vectors:
            profile_vector = np.mean(vectors, axis=0)
        else:
            profile_vector = np.zeros(course_embeddings.shape[1])

        student_vectors.append(profile_vector)

    return np.array(student_vectors)

def save_student_profiles(profiles, out_path='models/student_profiles.npy'):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    np.save(out_path, profiles)
    print(f"✅ Saved student profiles to {out_path}")

# ✅ New: One-liner for automatic retraining
def retrain_student_profiles(progress_path='data/student_progress.csv',
                              course_path='data/courses.csv',
                              embedding_path='models/course_embeddings.npy',
                              output_path='models/student_profiles.npy'):
    try:
        print("🔄 Training student profiles...")
        progress_df = pd.read_csv(progress_path)
        course_df = pd.read_csv(course_path)
        course_embeddings = np.load(embedding_path)

        profiles = build_student_profiles(progress_df, course_df, course_embeddings)
        save_student_profiles(profiles, output_path)

        print("✅ Student profiles updated.")
        return True, "Student profiles updated."
    except Exception as e:
        print(f"❌ Error during student profile training: {str(e)}")
        return False, f"Failed to update student profiles: {str(e)}"


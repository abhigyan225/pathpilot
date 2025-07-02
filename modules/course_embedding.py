import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import os

def load_courses(csv_path='data/courses.csv'):
    return pd.read_csv(csv_path)

def generate_course_embeddings(df, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(df['description'].fillna("").tolist())
    return df.reset_index(drop=True), embeddings

def save_embeddings(embeddings, out_path='models/course_embeddings.npy'):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    np.save(out_path, embeddings)
    print(f"✅ Saved embeddings to {out_path}")

def train_course_embeddings():
    try:
        print("🔄 Training course embeddings...")
        df = load_courses()
        df, embeddings = generate_course_embeddings(df)
        save_embeddings(embeddings)
        df.to_csv("data/courses.csv", index=False)  # optional: normalize saved data
        print("✅ Course embeddings updated.")
        return True, "Course embeddings updated."
    except Exception as e:
        print("❌ Error during course embedding:", str(e))
        return False, f"Failed to update course embeddings: {str(e)}"


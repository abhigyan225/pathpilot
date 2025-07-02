import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.course_embedding import load_courses, generate_course_embeddings, save_embeddings

# Load courses
df = load_courses("data/courses.csv")

# ✅ Generate embeddings (returns both df and embeddings)
df, embeddings = generate_course_embeddings(df)

# ✅ Save embeddings
save_embeddings(embeddings)


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.course_embedding import load_courses
from modules.student_profile import load_student_progress, build_student_profiles, save_student_profiles
import numpy as np

# Load course data and embeddings
course_df = load_courses('data/courses.csv')
course_embeddings = np.load('models/course_embeddings.npy')

# Load student progress
progress_df = load_student_progress('data/student_progress.csv')

# Build and save student profiles
student_profiles = build_student_profiles(progress_df, course_df, course_embeddings)
save_student_profiles(student_profiles)

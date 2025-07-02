import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.visualize import plot_most_completed_courses
import pandas as pd
# Load student progress
progress_df = pd.read_csv("data/student_progress.csv")

# Plot most completed courses
plot_most_completed_courses(progress_df, top_n=5)

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
print("✅ visualize.py loaded")

def plot_most_completed_courses(progress_df, top_n=5):
    """Plot top N most completed courses by all students."""
    all_courses = ",".join(progress_df['completed_courses']).split(",")
    course_counts = Counter(all_courses)

    top_courses = course_counts.most_common(top_n)
    courses, counts = zip(*top_courses)

    plt.figure(figsize=(8, 5))
    plt.bar(courses, counts, color='skyblue')
    plt.title(f"Top {top_n} Most Completed Courses")
    plt.xlabel("Course ID")
    plt.ylabel("Number of Completions")
    plt.tight_layout()
    plt.show()

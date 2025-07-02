import pandas as pd

def student_course_completion_rate(progress_df):
    """
    Calculate the average number of courses completed per student.
    """
    counts = progress_df['completed_courses'].apply(lambda x: len(x.split(',')) if pd.notna(x) else 0)
    return counts.mean()

def most_active_students(progress_df, top_n=5):
    """
    Return the top N most active students by number of completed courses.
    """
    df = progress_df.copy()
    df['completed_count'] = df['completed_courses'].apply(lambda x: len(x.split(',')) if pd.notna(x) else 0)
    return df.sort_values(by='completed_count', ascending=False).head(top_n)[['student_id', 'completed_courses', 'completed_count']]

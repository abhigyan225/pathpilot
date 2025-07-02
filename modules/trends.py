import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from flask import current_app

def parse_completion_trends(progress_df):
    """
    Returns a DataFrame with course completion counts grouped by month.
    
    Args:
        progress_df (pd.DataFrame): DataFrame with columns 'completed_courses' and 'completion_dates'.
    
    Returns:
        pd.DataFrame: DataFrame with columns ['course_id', 'month', 'count'] sorted by month.
    """
    course_date_counts = defaultdict(int)

    for _, row in progress_df.iterrows():
        courses = str(row['completed_courses']).split(',')
        dates = str(row['completion_dates']).split('|')

        for course, date_str in zip(courses, dates):
            if not date_str.strip():
                continue  # Skip empty dates
            try:
                date = pd.to_datetime(date_str.strip())
                month = date.strftime('%Y-%m')
                key = (course.strip(), month)
                course_date_counts[key] += 1
            except Exception:
                continue  # Skip invalid date formats

    trend_df = pd.DataFrame([
        {'course_id': course, 'month': month, 'count': count}
        for (course, month), count in course_date_counts.items()
    ])

    return trend_df.sort_values(by=['month', 'course_id']).reset_index(drop=True)

def plot_course_trends(trend_df, course_ids=None, save_path=None):
    """
    Plot course popularity over time for selected courses and save as an image.
    
    Args:
        trend_df (pd.DataFrame): DataFrame from parse_completion_trends.
        course_ids (list, optional): List of course IDs to filter on.
        save_path (str, optional): Path to save the plot image. If None, uses current_app.static_folder.
    """
    if course_ids:
        trend_df = trend_df[trend_df['course_id'].isin(course_ids)]

    pivot = trend_df.pivot(index='month', columns='course_id', values='count').fillna(0)
    pivot = pivot.sort_index()

    ax = pivot.plot(kind='line', marker='o', figsize=(10, 5))
    ax.set_title("📈 Course Completion Trends Over Time")
    ax.set_xlabel("Month")
    ax.set_ylabel("Completions")
    ax.grid(True)
    plt.tight_layout()

    if save_path is None:
        save_path = os.path.join(current_app.static_folder, "trend_plot.png")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    print("✅ Saving trend plot to:", save_path)

    plt.savefig(save_path)
    plt.close()

def plot_completion_heatmap(trend_df, save_path=None):
    """
    Plot a heatmap of course completions over months and save as image.
    
    Args:
        trend_df (pd.DataFrame): DataFrame from parse_completion_trends.
        save_path (str, optional): Path to save the heatmap image. If None, uses current_app.static_folder.
    """
    pivot = trend_df.pivot_table(index='course_id', columns='month', values='count', fill_value=0).astype(int)

    pivot = pivot.sort_index(axis=1)

    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt='d', cmap='YlGnBu', linewidths=0.5, cbar_kws={'label': 'Completions'})
    plt.title("🔥 Course Completion Heatmap")
    plt.xlabel("Month")
    plt.ylabel("Course ID")
    plt.tight_layout()

    if save_path is None:
        save_path = os.path.join(current_app.static_folder, "heatmap.png")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    print("✅ Saving heatmap to:", save_path)

    plt.savefig(save_path)
    plt.close()

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from modules.trends import (
    parse_completion_trends,
    plot_course_trends,
    plot_completion_heatmap  # ✅ Import all plotting functions together
)

# Load updated student progress CSV
progress_df = pd.read_csv("data/student_progress.csv")

# Parse trends
trend_df = parse_completion_trends(progress_df)
print("📊 Completion Trends DataFrame:\n", trend_df)
print("✅ Shape of trend_df:", trend_df.shape)

# ✅ Plot line chart for selected courses
plot_course_trends(trend_df, course_ids=['CS101', 'DS201', 'ML301'])

print("🔥 Plotting heatmap...")
plot_completion_heatmap(trend_df)
print("✅ Done plotting heatmap")
input("📌 Press Enter to exit...")

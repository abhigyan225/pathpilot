from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import yaml
import os
import csv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# === Import your custom modules ===
from modules.recommender import load_embeddings, recommend_courses_for_student
from modules.analytics import student_course_completion_rate, most_active_students
from modules.trends import parse_completion_trends, plot_course_trends, plot_completion_heatmap
from modules.visualize import plot_most_completed_courses

# === Flask App Setup ===
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "your_super_secret_key"

# === Load Data and Models at startup ===
course_df = pd.read_csv("data/courses.csv")
progress_df = pd.read_csv("data/student_progress.csv")
students_df = pd.read_csv("data/students.csv")
trend_df = parse_completion_trends(progress_df)
course_embeddings, student_profiles = load_embeddings()

# === ROUTES ===

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    recommendations = []
    student_id = None
    error = None
    no_courses = False
    all_courses = []

    # Load data
    course_df = pd.read_csv("data/courses.csv")
    progress_df = pd.read_csv("data/student_progress.csv")
    course_embeddings, student_profiles = load_embeddings()

    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip()
        
        student_row = progress_df[progress_df["student_id"] == student_id]

        if student_row.empty:
            error = "❌ Student does not exist."
        else:
            row = student_row.iloc[0]
            completed_courses = row.get("completed_courses")

            if pd.isna(completed_courses) or not str(completed_courses).strip():
                # No completed courses
                no_courses = True
                all_courses = course_df[["title", "description"]].to_dict(orient="records")
            else:
                # Get recommendations
                recommendations_df = recommend_courses_for_student(
                    student_id=student_id,
                    course_df=course_df,
                    course_embeddings=course_embeddings,
                    student_profiles=student_profiles,
                    top_n=5,
                    progress_df=progress_df
                )
                recommendations = recommendations_df.to_dict(orient="records")

    return render_template(
        "recommend.html",
        recommendations=recommendations,
        error=error,
        no_courses=no_courses,
        all_courses=all_courses,
        student_id=student_id
    )



@app.route("/analytics")
def analytics():
    avg = student_course_completion_rate(progress_df)
    top_students = most_active_students(progress_df).to_dict(orient="records")
    return render_template("analytics.html", average=avg, students=top_students)

@app.route("/trends")
def trends():
    generate = request.args.get("generate")
    if generate:
        progress_df = pd.read_csv("data/student_progress.csv")
        trend_df = parse_completion_trends(progress_df)
        plot_course_trends(trend_df)
        plot_completion_heatmap(trend_df)
        return render_template("trends.html", show_charts=True)
    else:
        return render_template("trends.html", show_charts=False)

@app.route("/top-courses")
def top_courses():
    df = pd.read_csv("data/courses.csv")
    top_enrolled = df.sort_values("enrollments", ascending=False).head(5)
    top_rated = df.sort_values("rating", ascending=False).head(5)
    return render_template(
        "top_courses.html",
        top_enrolled=top_enrolled.to_dict(orient="records"),
        top_rated=top_rated.to_dict(orient="records"),
    )

@app.route("/learning-path")
def learning_path():
    with open("data/learning_paths.yaml") as f:
        paths = yaml.safe_load(f)

    courses_df = pd.read_csv("data/courses.csv", encoding='utf-8-sig')
    id_to_title = dict(zip(courses_df.course_id, courses_df.title))

    path_courses = {
        role: [id_to_title.get(cid, cid) for cid in cids]
        for role, cids in paths.items()
    }

    return render_template("learning_path.html", paths=path_courses)

@app.route("/time-tracker")
def time_tracker():
    search_query = request.args.get("q", "").strip().lower()
    df = pd.read_csv("data/time_tracking.csv")

    pivot = (
        df.pivot_table(
            index="student_id",
            columns="task",
            values="hours_spent",
            aggfunc="sum",
            fill_value=0
        ).reset_index()
    )

    pivot["student_label"] = pivot["student_id"].apply(lambda x: f"Student {x}")

    if search_query:
        pivot = pivot[pivot["student_label"].str.lower().str.contains(search_query)]
        time_data = pivot.to_dict(orient="records")
    else:
        time_data = []

    tasks = list(pivot.columns)
    for col in ["student_id", "student_label"]:
        if col in tasks:
            tasks.remove(col)

    return render_template("time_tracker.html", time_data=time_data, task_columns=tasks, search_query=search_query)

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_id = request.form["admin_id"]
        password = request.form["password"]
        if admin_id == "admin" and password == "password123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")

from flask import render_template, request, redirect, url_for, flash, session
import os
from modules.course_embedding import train_course_embeddings
from modules.student_profile import retrain_student_profiles

@app.route("/admin-dashboard", methods=["GET", "POST"])
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        files = {
            "courses.csv": request.files.get("courses_file"),
            "learning_paths.yaml": request.files.get("learning_paths_file"),
            "student_progress.csv": request.files.get("student_progress_file"),
            "time_tracking.csv": request.files.get("time_tracking_file"),
            "students.csv": request.files.get("students_file")  # NEW: handle students.csv
        }

        # Flags to track which files were updated
        updated_courses = False
        updated_students = False
        updated_progress = False

        for filename, file in files.items():
            if file and file.filename:
                save_path = os.path.join("data", filename)
                file.save(save_path)
                flash(f"✅ {filename} uploaded successfully and replaced the previous version.", "success")

                if filename == "courses.csv":
                    updated_courses = True
                elif filename == "students.csv":
                    updated_students = True
                elif filename == "student_progress.csv":
                    updated_progress = True

        # === Re-train course embeddings ===
        if updated_courses:
            success, message = train_course_embeddings()
            flash(("🧠 " if success else "❌ ") + message, "success" if success else "error")

        # === Re-train student profiles ===
        if updated_students or updated_progress:
            success, message = retrain_student_profiles()
            flash(("👥 " if success else "❌ ") + message, "success" if success else "error")

        return redirect(url_for("admin_dashboard"))

    return render_template("admin_dashboard.html")



from modules.student_profile import retrain_student_profiles  # 👈 Add at top

@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        student_id = request.form["student_id"].strip()
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        students_df = pd.read_csv("data/students.csv", dtype=str)
        students_df = students_df.dropna(subset=["student_id"])
        students_df["student_id"] = students_df["student_id"].str.strip()
        students_df = students_df[students_df["student_id"] != ""]
        students_df.to_csv("data/students.csv", index=False)

        existing_ids = students_df["student_id"].astype(str).str.strip().tolist()
        if student_id in existing_ids:
            flash("❌ Student ID already exists!", "error")
        else:
            students_df = pd.concat([
                students_df,
                pd.DataFrame([{
                    "student_id": student_id,
                    "username": username,
                    "password": password
                }])
            ], ignore_index=True)
            students_df.to_csv("data/students.csv", index=False)

            # ✅ Update student progress
            progress_df = pd.read_csv("data/student_progress.csv", dtype=str)
            new_row = {
                "student_id": student_id,
                "completed_courses": "",
                "completion_dates": "",
                "time_spent_hours": ""
            }
            progress_df = pd.concat([progress_df, pd.DataFrame([new_row])], ignore_index=True)
            progress_df.to_csv("data/student_progress.csv", index=False)

            # ✅ Retrain student profiles
            retrain_student_profiles()

            flash("✅ New student added successfully!", "success")
            return redirect(url_for("admin_dashboard"))

    return render_template("add_student.html")

from modules.course_embedding import train_course_embeddings  # Add this at the top

@app.route("/add-course", methods=["GET", "POST"])
def add_course():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        course_id = request.form["course_id"].strip()
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        enrollments = request.form["enrollments"].strip()
        rating = request.form["rating"].strip()

        df = pd.read_csv("data/courses.csv", dtype=str)
        if course_id in df["course_id"].values:
            flash("❌ Course ID already exists!", "error")
        else:
            new_row = {
                "course_id": course_id,
                "title": title,
                "description": description,
                "enrollments": enrollments or "0",
                "rating": rating or "0"
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv("data/courses.csv", index=False)
            flash("✅ Course added successfully!", "success")

            # 🔁 Automatically regenerate course embeddings
            train_course_embeddings()

            return redirect(url_for("admin_dashboard"))

    return render_template("add_course.html")


@app.route("/student-login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        print("Submitted:", repr(username), repr(password))

        students_df = pd.read_csv("data/students.csv", dtype=str)
        students_df = students_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        print("Loaded usernames:", students_df['username'].tolist())
        print("Loaded passwords:", students_df['password'].tolist())

        student = students_df[
            (students_df["username"] == username) &
            (students_df["password"] == password)
        ]

        print("Matched student:", student)

        if not student.empty:
            session["student_logged_in"] = True
            session["student_id"] = student.iloc[0]["student_id"]
            session["username"] = username
            return redirect(url_for("student_dashboard"))
        else:
            flash("Invalid credentials", "error")

    return render_template("student_login.html")

from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from datetime import datetime

from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

from datetime import datetime

from flask import render_template, request, redirect, url_for, session
import pandas as pd
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, session
import pandas as pd
from datetime import datetime

from modules.student_profile import retrain_student_profiles  # 👈 Add at top

@app.route('/student-dashboard', methods=['GET', 'POST'])
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    student_id = session['student_id']
    student_name = session.get('student_name', 'Student')

    progress_path = 'data/student_progress.csv'
    courses_path = 'data/courses.csv'
    tracking_path = 'data/time_tracking.csv'

    progress_df = pd.read_csv(progress_path)
    courses_df = pd.read_csv(courses_path)

    if student_id not in progress_df['student_id'].values:
        new_row = pd.DataFrame([{
            'student_id': student_id,
            'completed_courses': '',
            'completion_dates': '',
            'time_spent_hours': ''
        }])
        progress_df = pd.concat([progress_df, new_row], ignore_index=True)
        progress_df.to_csv(progress_path, index=False)

    student_row = progress_df[progress_df['student_id'] == student_id].iloc[0]

    success = False
    if request.method == 'POST':
        completed_courses = request.form.getlist("completed_courses")
        today_str = datetime.now().strftime("%Y-%m-%d")

        if completed_courses:
            prev_courses = [c.strip() for c in str(student_row.get('completed_courses', '')).split(',') if c.strip()]
            prev_dates = str(student_row.get('completion_dates', '')).split('|') if pd.notna(student_row.get('completion_dates')) else []
            prev_times = str(student_row.get('time_spent_hours', '')).split('|') if pd.notna(student_row.get('time_spent_hours')) else []

            new_logs = []

            for course_id in completed_courses:
                time_val = request.form.get(f"time_{course_id}", "0")
                try:
                    time_val_float = float(time_val)
                except ValueError:
                    time_val_float = 0.0

                new_logs.append({
                    "student_id": student_id,
                    "date": today_str,
                    "hours_spent": str(time_val_float),
                    "task": f"Completed {course_id}"
                })

                if course_id not in prev_courses:
                    prev_courses.append(course_id)
                    prev_dates.append(today_str)
                    prev_times.append(str(time_val_float))

            progress_df.loc[progress_df['student_id'] == student_id, 'completed_courses'] = ",".join(prev_courses)
            progress_df.loc[progress_df['student_id'] == student_id, 'completion_dates'] = "|".join(prev_dates)
            progress_df.loc[progress_df['student_id'] == student_id, 'time_spent_hours'] = "|".join(prev_times)
            progress_df.to_csv(progress_path, index=False)

            try:
                tracking_df = pd.read_csv(tracking_path, dtype=str)
            except FileNotFoundError:
                tracking_df = pd.DataFrame(columns=["student_id", "date", "hours_spent", "task"])

            if new_logs:
                tracking_df = pd.concat([tracking_df, pd.DataFrame(new_logs)], ignore_index=True)
                tracking_df.to_csv(tracking_path, index=False)

            # ✅ Retrain student profiles after update
            retrain_student_profiles()

            success = True

    student_row = progress_df[progress_df['student_id'] == student_id].iloc[0]

    raw_courses = student_row.get('completed_courses', '')
    if pd.isna(raw_courses):
        raw_courses = ''
    completed = [c.strip() for c in str(raw_courses).split(',') if c.strip() and c.strip().lower() != 'nan']

    raw_times = student_row.get('time_spent_hours', '')
    if pd.isna(raw_times):
        raw_times = ''
    time_spent_map = dict(zip(completed, str(raw_times).split("|"))) if raw_times else {}

    if completed:
        recommended_df = courses_df[~courses_df['course_id'].isin(completed)]
        recommended = recommended_df.to_dict(orient='records')

        return render_template("student_dashboard.html",
                               student_name=student_name,
                               completed=completed,
                               recommended=recommended,
                               time_spent=time_spent_map,
                               success=success)
    else:
        return render_template("student_dashboard_new.html",
                               student_name=student_name,
                               selected_courses=[],
                               time_spent={},
                               all_courses=courses_df.to_dict(orient='records'),
                               progress=0,
                               success=success)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("student_login"))

import csv
import pandas as pd

def search_courses(query):
    df = pd.read_csv("data/courses.csv")
    query = query.lower()
    results = df[
        df["title"].str.lower().str.contains(query) |
        df["course_id"].str.lower().str.contains(query)
    ]
    return results[["course_id", "title", "description"]].to_dict(orient="records")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    courses = search_courses(query) if query else []
    return render_template("search.html", query=query, courses=courses)



@app.route("/visualize")
def visualize():
    plot_most_completed_courses(progress_df)
    return render_template("trends.html")


@app.route("/static-test")
def static_test():
    return '<link rel="stylesheet" href="/static/style.css">'

if __name__ == "__main__":
    app.run(debug=True)

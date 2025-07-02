
# 🧠 PathPilot — AI-Powered Learning Path Recommender

PathPilot is a smart, personalized learning platform that recommends courses and learning paths to students based on their progress, interests, and performance. Built with Flask, Python, and machine learning, this system is perfect for educational platforms and online academies looking to deliver personalized, data-driven learning journeys.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 🚀 Features

- 🔐 **Admin & Student Portals**  
  Separate login for students and administrators with appropriate access controls.

- 🧩 **Intelligent Course Recommendations**  
  Uses content-based filtering with embeddings to suggest personalized next-step courses.

- 🛠️ **Dynamic Course & Student Management**  
  Admins can upload or update CSV/YAML files to overwrite the full database or add new entries manually.

- 📈 **Learning Path Mapping**  
  Students get guided learning paths (e.g., Data Scientist, AI Engineer) based on YAML-defined sequences.

- 📊 **Student Progress Tracking**  
  Visualizes time spent, course completion, and progress trends using student activity data.

- 🧠 **On-Demand Model Re-Training**  
  Whenever a student/course/progress dataset is updated, embeddings and student profiles are automatically retrained.

---

## 📁 Project Structure

```
├── app/                      # Main Flask app
│   ├── routes.py             # Flask routes
│   ├── templates/            # HTML templates (Jinja2)
│   ├── static/               # CSS / images / JS
│   └── modules/              # ML logic
│       ├── course_embedding.py
│       ├── student_profile.py
│       └── visualize.py
├── data/                     # CSV / YAML data files
│   ├── courses.csv
│   ├── students.csv
│   ├── student_progress.csv
│   ├── time_tracking.csv
│   └── learning_paths.yaml
├── models/                   # Saved embeddings
│   └── course_embeddings.npy
├── README.md
├── requirements.txt
└── run.py                    # Entry point
```

---

## 📦 Data Files

The system uses structured data stored in CSV and YAML format. Here's a quick overview:

### ✅ `courses.csv`
```csv
course_id,title,description,enrollments,rating
CS101,Python for Beginners,"Learn basic Python programming...",120,4.5
```

### ✅ `students.csv`
```csv
student_id,name,password
S001,Alice,pass123
```

### ✅ `student_progress.csv`
```csv
student_id,completed_courses,completion_dates,time_spent_hours
S001,"['CS101']", "['2024-07-01']", 12.5
```

### ✅ `time_tracking.csv`
```csv
student_id,date,hours_spent,task
S001,2024-07-01,2.5,"Watched Module 1"
```

### ✅ `learning_paths.yaml`
```yaml
Data Scientist:
  - CS101
  - DS201
  - ML301
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/abhigyan225/pathpilot.git
cd pathpilot
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate # On Unix/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
flask run
```

Open your browser and go to `http://127.0.0.1:5000`

---

## 🧪 Example Use Cases

- Educational platforms offering adaptive learning
- Internal LMS for corporations with skill-mapping
- Bootcamps and academies with sequenced curriculum

---

## 🛡️ Admin Panel Features

Accessible at `/admin-login` (with basic session-based authentication). From the dashboard, you can:

- Add new students or courses manually
- Upload full datasets (`.csv`, `.yaml`) to replace old data
- Re-train the recommendation model with one click

---

## 📊 Student Dashboard

Students can:
- Login securely
- View their completed courses
- Get real-time personalized course suggestions
- Visualize their time investment

---

## 🤖 Recommendation Engine

Uses vector embeddings to compute similarity between student learning profiles and course representations.

- `course_embedding.py`: Generates embeddings from course content
- `student_profile.py`: Builds personalized vectors for students based on their activity

---

## 👨‍💻 Contributing

Pull requests are welcome! If you’d like to suggest a feature or report a bug, open an issue first.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🌐 Author

Built with ❤️ by Abhigyan bajpai

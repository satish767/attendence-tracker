from flask import Flask, render_template, request, jsonify, session, redirect
import qrcode
import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecret'

USERS_FILE = 'users.json'
DATA_FILE = 'data.json'
SUBJECTS_FILE = 'subjects.json'

# ---------- Utility Functions ----------
def load_users():
    if not os.path.exists(USERS_FILE):
        return {"users": []}
    with open(USERS_FILE) as f:
        return json.load(f)

def find_user(email):
    users = load_users()["users"]
    return next((u for u in users if u["email"] == email), None)

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"attendance": {}}, f)
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_subjects():
    if not os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, 'w') as f:
            json.dump({"subjects": []}, f)
    with open(SUBJECTS_FILE) as f:
        return json.load(f).get("subjects", [])

# ---------- Routes ----------

@app.route('/')
def index():
    return redirect('/select_login')

@app.route('/select_login')
def select_login():
    return render_template('select_login.html')

@app.route('/login/<role>')
def login_page(role):
    return render_template('login.html', role=role)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')

    user = find_user(email)
    if user and user["password"] == password and user["role"] == role:
        session['email'] = email
        session['role'] = role
        return redirect('/admin' if role == 'admin' else '/student')
    return "Invalid email, password, or role"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/select_login')

# ---------- Admin ----------

@app.route('/admin')
def admin():
    if session.get("role") != "admin":
        return redirect('/select_login')

    with open('subjects.json') as f:
        subjects = json.load(f)["subjects"]
    return render_template('admin.html', email=session["email"], subjects=subjects)


@app.route('/get_subjects')
def get_subjects():
    with open('subjects.json') as f:
        subjects = json.load(f)["subjects"]
    return jsonify({"subjects": subjects})

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.get_json()
    subject_id = data.get("subject")
    if not subject_id:
        return jsonify({"success": False, "error": "No subject provided"}), 400

    today = datetime.date.today().isoformat()
    qr_text = f"{subject_id}::{today}"

    qr = qrcode.make(qr_text)
    qr.save("static/qr.png")
    return jsonify({"success": True, "date": today})


# ---------- Student ----------

@app.route('/student')
def student():
    if session.get("role") != "student":
        return redirect('/select_login')
    
    user = find_user(session.get("email"))
    return render_template('student.html', name=user.get("name", "Student"), email=user["email"])

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if session.get("role") != "student":
        return jsonify({"error": "Unauthorized"}), 401

    student_email = session.get("email")
    data = request.get_json()
    
    try:
        subject_id, date = data['qr'].split("::")
    except:
        return jsonify({"error": "Invalid QR format"}), 400

    attendance = load_data()
    if date not in attendance["attendance"]:
        attendance["attendance"][date] = {}
    if subject_id not in attendance["attendance"][date]:
        attendance["attendance"][date][subject_id] = []
    if student_email not in attendance["attendance"][date][subject_id]:
        attendance["attendance"][date][subject_id].append(student_email)

    save_data(attendance)
    return jsonify({"status": "marked", "subject": subject_id, "date": date})

@app.route('/get_attendance')
def get_attendance():
    return jsonify(load_data())

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True, port=5001)

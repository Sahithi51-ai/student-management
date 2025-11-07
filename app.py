from typing import Any
from flask import Flask, render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(20), nullable=False)
    student_class = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
@app.route('/')
def home():
    return render_template('index.html', std=students)
@app.route('/add', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        student_class = request.form['class']
        email = request.form['email']

        new_id = len(students) + 1
        students.append({
            "id": new_id,
            "name": name,
            "roll": roll,
            "class": student_class,
            "email": email
        })

        return redirect(url_for('home'))
    
    return render_template('add.html')

# 🗑️ DELETE STUDENT
@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('home'))


# ✏️ UPDATE STUDENT
@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    # logic here
    pass

    for student in students:
        if student['id'] == student_id:
            if request.method == 'POST':
                student['name'] = request.form['name']
                student['roll'] = request.form['roll']
                student['class'] = request.form['class']
                student['email'] = request.form['email']
                return redirect(url_for('home'))
            return render_template('update.html', student=student)
    return "Student not found", 404




@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

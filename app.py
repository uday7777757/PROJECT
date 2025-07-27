from flask import Flask, render_template, request,redirect
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'students.db'

# ---------- DATABASE SETUP ----------
def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll TEXT NOT NULL,
                    math INTEGER NOT NULL,
                    physics INTEGER NOT NULL,
                    biology INTEGER NOT NULL
                )
            ''')
            conn.commit()

# ---------- ROUTES ----------
@app.route('/')
def func():
    return render_template('dashboard.html')
@app.route('/add-student',methods=['POST'])
def student_form():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        math = int(request.form['math'])
        physics = int(request.form['physics'])
        biology = int(request.form['biology'])

        # Save to database
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO students (name, roll, math, physics, biology)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, roll, math, physics, biology))
            conn.commit()

        total = math + physics + biology
        avg = total / 3
        return (f"""<h2 style=text_alignment:center;> your entry sucessfully added</h2>""")

@app.route('/view',methods=['GET','PUT','DELETE'])
def view():
    if request.method == 'PUT':
        name = request.form['name']
        roll = request.form['roll']
        math = int(request.form['math'])
        physics = int(request.form['physics'])
        biology = int(request.form['biology'])



@app.route('/students',methods = ['GET'])
def students():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''
        select * from students

    ''')
        students = c.fetchall()
        conn.commit()
    return render_template('dashboard.html',students=students)
            
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM students WHERE id = ?", (id,))
        conn.commit()
    return redirect('/students')




@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()

        if request.method == 'POST':
            try:
                name = request.form['name']
                roll = request.form['roll']
                math = int(request.form['math'])
                physics = int(request.form['physics'])
                biology = int(request.form['biology'])

                c.execute('''
                    UPDATE students
                    SET name = ?, roll = ?, math = ?, physics = ?, biology = ?
                    WHERE id = ?
                ''', (name, roll, math, physics, biology, id))
                conn.commit()
                return redirect('/students')
            except Exception as e:
                return f"<p>Error: {str(e)}</p>"

        # Handle GET
        c.execute('SELECT * FROM students WHERE id = ?', (id,))
        student = c.fetchone()
        if student:
            return render_template('edit.html', student=student)
        else:
            return f"<p>No student found with ID {id}</p>"

#     return render_template("index.html")
# @app.route('/students',methods = ['GET'])
# def student_data():
#     if request.method == 'GET':
#         with sqlite3.connect(DATABASE) as conn:
#             c = conn.cursor()
#             c.execute('''
#             select * from students
# ''')
#             students = c.fetchall()
#             conn.commit()
#         html = "<h2>All Students</h2><table border='1' cellpadding='8'>"
#         html += "<tr><th>ID</th><th>Name</th><th>Roll</th><th>Math</th><th>Physics</th><th>Biology</th></tr>"

#         for s in students:
#             html += f"<tr><td>{s[0]}</td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td><td>{s[4]}</td><td>{s[5]}</td></tr>"

#         html += "</table><br><a href='/'>Back to form</a>"
#         return html
#     return redirect('/')
# @app.route('/maxmarks',methods = ["GET"])
# def f():
#     if request.method == "GET":
#         with sqlite3.connect(DATABASE) as conn:
#             c = conn.cursor()
#             c.execute('''
#             select name,MAX(math) from students
# ''')
#             student = c.fetchone()
#             conn.commit()
#     return f"<p>{student[0]} got highst marks in physics {student[1]}</p>"
# @app.route('/id-route',methods = ['POST','GET'])
# def id_to():
#     if request.method == 'POST':
#         sid = request.form['id']
#     try:
#         with sqlite3.connect(DATABASE) as conn:
#             c = conn.cursor()
#             c.execute('''
#             select * from students where id = ?
# ''',(sid,))
#             student = c.fetchone()
#         if student:
#             return f'<p>Student ID: {student[0]} | Name: {student[1]} | Roll: {student[2]} | Math: {student[3]} | Physics: {student[4]} | Biology: {student[5]}</p>'
#         return f'<p>id not found </p>'
#     except Exception as e:
#         return f'<p>id not found{e}</p>'


# ---------- MAIN ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
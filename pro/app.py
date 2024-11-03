from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the database (use SQLite for simplicity here)
DATABASE = 'feedback.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class INTEGER NOT NULL,
                section TEXT NOT NULL,
                date TEXT NOT NULL,
                form teacher TEXT NOT NULL,
                subject TEXT NOT NULL,
                ques1 INTEGER NOT NULL,
                ques2i INTEGER NOT NULL,
                ques2ii INTEGER NOT NULL,
                ques2iii INTEGER NOT NULL,
                ques2iv INTEGER NOT NULL,
                ques2v INTEGER NOT NULL,
                ques3 INTEGER NOT NULL,
                ques4 INTEGER NOT NULL,
                remarks TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        db.commit()

@app.before_request
def create_tables():
    init_db()

# Route to render the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to render the feedback form
@app.route('/feedback_form')
def feedback_form():
    return render_template('feedback_form.html')

# Route to handle feedback form submission
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.form
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (class, section, date, form teacher, subject, ques1, ques2i, ques2ii, ques2iii, ques2iv, ques2v, ques3, ques4, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['class'], data['section'], data['date'], data['form teacher'], data['subject'], data['ques1'], data['ques2i'], data['ques2ii'], data['ques2iii'], data['ques2iv'], data['ques2v'], data['ques3'], data['ques4'], data['remarks']))
    conn.commit()
    return redirect(url_for('home'))

# Route to render the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('admin'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

# Route to render the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

# Route to render the admin page
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback')
    feedbacks = cursor.fetchall()
    return render_template('admin.html', feedbacks=feedbacks)

# Route to add new feedback entry
@app.route('/feedback', methods=['POST'])
def add_feedback():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO feedback (class, section, date, form teacher, subject, ques1, ques2i, ques2ii, ques2iii, ques2iv, ques2v, ques3, ques4, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['class'], data['section'], data['date'], data['form teacher'], data['subject'], data['ques1'], data['ques2i'], data['ques2ii'], data['ques2iii'], data['ques2iv'], data['ques2v'], data['ques3'], data['ques4'], data['remarks']))
    conn.commit()
    return jsonify({'message': 'Feedback added successfully'}), 201

# Route to add a new user
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user (email, password)
        VALUES (?, ?)
    ''', (data['email'], generate_password_hash(data['password'], method='pbkdf2:sha256')))
    conn.commit()
    return jsonify({'message': 'User added successfully'}), 201

# Route to retrieve all feedback
@app.route('/feedback', methods=['GET'])
def get_feedback():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback')
    feedback_list = cursor.fetchall()
    feedback_data = []
    for feedback in feedback_list:
        feedback_data.append({
            'id': feedback['id'],
            'class': feedback['class'],
            'section': feedback['section'],
            'date': feedback['date'],
            'form teacher': feedback['form teacher'],
            'subject': feedback['subject'],
            'ques1': feedback['ques1'],
            'ques2i': feedback['ques2i'],
            'ques2ii': feedback['ques2ii'],
            'ques2iii': feedback['ques2iii'],
            'ques2iv': feedback['ques2iv'],
            'ques2v': feedback['ques2v'],
            'ques3': feedback['ques3'],
            'ques4': feedback['ques4'],
            'remarks': feedback['remarks']
        })
    return jsonify(feedback_data)

# Route to retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()
    users_data = [{'id': user['id'], 'email': user['email']} for user in users]
    return jsonify(users_data)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Micky@:3",
    database="schemes_db"
)

@app.route('/')
def landing():
    return render_template("home.html")

@app.route('/check-form')
def form():
    return render_template("index.html")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/check', methods=['POST'])
def check():
    education = request.form['education']
    income = int(request.form['income'])
    category = request.form['category']
    gender = request.form['gender']
    age = int(request.form['age'])

    cursor = db.cursor(dictionary=True)

    query = """
    SELECT * FROM schemes
    WHERE education_level = %s
    AND max_income >= %s
    AND (category = %s OR category = 'Any')
    AND (gender = %s OR gender = 'Any')
    AND min_age <= %s
    AND max_age >= %s
    """

    cursor.execute(query, (education, income, category, gender, age, age))
    results = cursor.fetchall()

    return render_template("result.html", schemes=results)

@app.route('/admin')
def admin():
    return render_template("admin_login.html")


@app.route('/admin-login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    # Simple hardcoded authentication
    if username == "admin" and password == "admin123":
        return render_template("admin_dashboard.html")
    else:
        return "<h3>Invalid Credentials</h3><a href='/admin'>Try Again</a>"
    
@app.route('/add-scheme')
def add_scheme():
    return render_template("add_scheme.html")


@app.route('/save-scheme', methods=['POST'])
def save_scheme():
    scheme_name = request.form['scheme_name']
    education = request.form['education']
    max_income = int(request.form['max_income'])
    category = request.form['category']
    gender = request.form['gender']
    min_age = int(request.form['min_age'])
    max_age = int(request.form['max_age'])
    benefits = request.form['benefits']
    documents = request.form['documents']

    cursor = db.cursor()

    query = """
    INSERT INTO schemes 
    (scheme_name, education_level, max_income, category, gender, min_age, max_age, benefits, documents)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (scheme_name, education, max_income, category, gender, min_age, max_age, benefits, documents))
    db.commit()

    return "<h3>Scheme Added Successfully!</h3><a href='/admin'>Back to Dashboard</a>"

if __name__ == '__main__':
    app.run(debug=True)
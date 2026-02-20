from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Micky@:3",
    database="schemes_db"
)

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

if __name__ == '__main__':
    app.run(debug=True)
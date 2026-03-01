from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

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

@app.route('/check', methods=['POST'])
def check():
    education = request.form['education']
    income = int(request.form['income'])
    category = request.form['category']
    gender = request.form['gender']
    disability = request.form['disability']
    age = int(request.form['age'])

    if age < 5:
        flash("Invalid Age Entered")
        return redirect(url_for('form'))

    if income < 0:
        flash("Income Cannot Be Negative")
        return redirect(url_for('form'))
    
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT * FROM schemes
    WHERE education_level = %s
    AND max_income >= %s
    AND (category = %s OR category = 'Any')
    AND (gender = %s OR gender = 'Any')
    AND (disability = %s OR disability = 'Any')
    AND min_age <= %s
    AND max_age >= %s
    """

    cursor.execute(query, (education, income, category, gender, disability, age, age))
    results = cursor.fetchall()

    return render_template("result.html", schemes=results)

@app.route('/admin')
def admin():
    return render_template("admin_login.html")


@app.route('/admin-login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "admin123":
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        return "Invalid Credentials"
    
@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin_logged_in' in session:
        cursor = db.cursor(dictionary=True)

        # Fetch schemes (search support remains)
        search_query = request.args.get('search')

        if search_query:
            cursor.execute("SELECT * FROM schemes WHERE scheme_name LIKE %s",
                           ('%' + search_query + '%',))
        else:
            cursor.execute("SELECT * FROM schemes")

        schemes = cursor.fetchall()

        # 📊 Statistics
        cursor.execute("SELECT COUNT(*) as total FROM schemes")
        total_schemes = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) as ug_count FROM schemes WHERE education_level = 'UG'")
        ug_count = cursor.fetchone()['ug_count']

        cursor.execute("SELECT COUNT(*) as pg_count FROM schemes WHERE education_level = 'PG'")
        pg_count = cursor.fetchone()['pg_count']

        cursor.execute("SELECT COUNT(*) as pwd_count FROM schemes WHERE disability = 'Yes'")
        pwd_count = cursor.fetchone()['pwd_count']

        return render_template(
            "admin_dashboard.html",
            schemes=schemes,
            total_schemes=total_schemes,
            ug_count=ug_count,
            pg_count=pg_count,
            pwd_count=pwd_count
        )
    else:
        return redirect(url_for('admin'))
    
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin'))

@app.route('/scheme/<int:id>')
def scheme_detail(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schemes WHERE id = %s", (id,))
    scheme = cursor.fetchone()
    return render_template("scheme_detail.html", scheme=scheme)

@app.route('/add-scheme')
def add_scheme():
    if 'admin_logged_in' in session:
        return render_template("add_scheme.html")
    else:
        return redirect(url_for('admin'))
    
@app.route('/delete-scheme/<int:id>')
def delete_scheme(id):
    if 'admin_logged_in' in session:
        cursor = db.cursor()
        cursor.execute("DELETE FROM schemes WHERE id = %s", (id,))
        db.commit()
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('admin'))
    
@app.route('/edit-scheme/<int:id>')
def edit_scheme(id):
    if 'admin_logged_in' in session:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM schemes WHERE id = %s", (id,))
        scheme = cursor.fetchone()
        return render_template("edit_scheme.html", scheme=scheme)
    else:
        return redirect(url_for('admin'))
    
@app.route('/update-scheme/<int:id>', methods=['POST'])
def update_scheme(id):
    if 'admin_logged_in' in session:

        scheme_name = request.form['scheme_name']
        education = request.form['education']
        max_income = request.form['max_income']
        category = request.form['category']
        gender = request.form['gender']
        disability = request.form['disability']
        min_age = request.form['min_age']
        max_age = request.form['max_age']
        benefits = request.form['benefits']
        documents = request.form['documents']
        official_link = request.form['official_link']
        youtube_link = request.form['youtube_link']

        cursor = db.cursor()

        query = """
        UPDATE schemes
        SET scheme_name=%s,
            education_level=%s,
            max_income=%s,
            category=%s,
            gender=%s,
            disability=%s,
            min_age=%s,
            max_age=%s,
            benefits=%s,
            documents=%s,
            official_link=%s,
            youtube_link=%s
        WHERE id=%s
        """

        cursor.execute(query, (
            scheme_name, education, max_income, category,
            gender,disability, min_age, max_age,
            benefits, documents,
            official_link, youtube_link,
            id
        ))

        db.commit()

        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('admin'))

@app.route('/save-scheme', methods=['POST'])
def save_scheme():
    if 'admin_logged_in' in session:

        scheme_name = request.form['scheme_name']
        education = request.form['education']
        max_income = int(request.form['max_income'])
        category = request.form['category']
        gender = request.form['gender']
        min_age = int(request.form['min_age'])
        max_age = int(request.form['max_age'])
        benefits = request.form['benefits']
        documents = request.form['documents']
        disability = request.form['disability']
        official_link = request.form['official_link']
        youtube_link = request.form['youtube_link']

        cursor = db.cursor()

        query = """
        INSERT INTO schemes 
        (scheme_name, education_level, max_income, category, gender,
        min_age, max_age, benefits, documents, official_link, youtube_link, disability)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            scheme_name, education, max_income,
            category, gender,
            min_age, max_age,
            benefits, documents,
            official_link, youtube_link,
            disability
        ))

        db.commit()

        return redirect(url_for('admin_dashboard'))

    else:
        return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
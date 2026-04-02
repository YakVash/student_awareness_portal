from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Seetha0987@",
    database="schemes_db"
)


# HOME PAGE
@app.route('/')
def landing():

    cursor = db.cursor(dictionary=True)

    # Total schemes
    cursor.execute("SELECT COUNT(*) as total FROM schemes")
    total_schemes = cursor.fetchone()['total']

    # UG schemes
    cursor.execute("SELECT COUNT(*) as ug FROM schemes WHERE education_level='UG'")
    ug_count = cursor.fetchone()['ug']

    # PG schemes
    cursor.execute("SELECT COUNT(*) as pg FROM schemes WHERE education_level='PG'")
    pg_count = cursor.fetchone()['pg']

    # Sports schemes
    cursor.execute("SELECT COUNT(*) as sports FROM schemes WHERE sports='Yes'")
    sports_count = cursor.fetchone()['sports']

    # PWD schemes
    cursor.execute("SELECT COUNT(*) as pwd FROM schemes WHERE disability='Yes'")
    pwd_count = cursor.fetchone()['pwd']

    # Minority schemes
    cursor.execute("SELECT COUNT(*) as minority FROM schemes WHERE category='Minority'")
    minority_count = cursor.fetchone()['minority']

    # Women schemes
    cursor.execute("SELECT COUNT(*) as women FROM schemes WHERE gender='Female'")
    women_count = cursor.fetchone()['women']

    cursor.execute("SELECT * FROM schemes ORDER BY id DESC LIMIT 4")
    featured_schemes = cursor.fetchall()

    return render_template(
        "home.html",
        total_schemes=total_schemes,
        ug_count=ug_count,
        pg_count=pg_count,
        sports_count=sports_count,
        pwd_count=pwd_count,
        minority_count=minority_count,
        women_count=women_count,
        featured_schemes=featured_schemes
    )


# SEARCH ROUTE (used by homepage search form)
@app.route('/search')
def search():

    query = request.args.get('query', '')

    cursor = db.cursor(dictionary=True)

    if query:
        search_query = "SELECT * FROM schemes WHERE scheme_name LIKE %s OR benefits LIKE %s OR category LIKE %s"
        search_term = '%' + query + '%'
        cursor.execute(search_query, (search_term, search_term, search_term))
    else:
        cursor.execute("SELECT * FROM schemes ORDER BY scheme_name")

    schemes = cursor.fetchall()

    return render_template("all_schemes.html", schemes=schemes)


# ELIGIBILITY FORM
@app.route('/check-form')
def form():
    return render_template("index.html")


# CHECK ELIGIBILITY
@app.route('/check', methods=['POST'])
def check():

    education = request.form['education']
    income = int(request.form['income'])
    category = request.form['category']
    gender = request.form['gender']
    disability = request.form['disability']
    first_graduate = request.form['first_graduate']
    age = int(request.form['age'])

    if age < 5:
        flash("Invalid Age Entered", "error")
        return redirect(url_for('form'))

    if income < 0:
        flash("Income Cannot Be Negative", "error")
        return redirect(url_for('form'))

    cursor = db.cursor(dictionary=True)

    query = """
    SELECT * FROM schemes
    WHERE (education_level = %s OR education_level = 'Any')
    AND max_income >= %s
    AND (category = %s OR category = 'Any')
    AND (gender = %s OR gender = 'Any')
    AND (disability = %s OR disability = 'Any')
    AND (first_graduate = %s OR first_graduate = 'Any')
    AND min_age <= %s
    AND max_age >= %s
    """

    cursor.execute(query, (education, income, category, gender, disability, first_graduate, age, age))
    results = cursor.fetchall()

    return render_template("result.html", schemes=results)


# ADMIN LOGIN PAGE
@app.route('/admin')
def admin():
    return render_template("admin_login.html")


# ADMIN LOGIN
@app.route('/admin-login', methods=['POST'])
def admin_login():

    username = request.form['username']
    password = request.form['password']

    if username == "admin" and password == "admin123":
        session['admin_logged_in'] = True
        flash("Welcome back, Admin!", "success")
        return redirect(url_for('admin_dashboard'))
    else:
        flash("Invalid Credentials. Please try again.", "error")
        return redirect(url_for('admin'))


# ADMIN DASHBOARD
@app.route('/admin-dashboard')
def admin_dashboard():

    if 'admin_logged_in' not in session:
        return redirect(url_for('admin'))

    cursor = db.cursor(dictionary=True)

    filter_type = request.args.get('filter')

    if filter_type == "UG":
        cursor.execute("SELECT * FROM schemes WHERE education_level='UG'")

    elif filter_type == "PG":
        cursor.execute("SELECT * FROM schemes WHERE education_level='PG'")

    elif filter_type == "PWD":
        cursor.execute("SELECT * FROM schemes WHERE disability='Yes'")

    elif filter_type == "Sports":
        cursor.execute("SELECT * FROM schemes WHERE sports='Yes'")

    elif filter_type == "Caste":
        cursor.execute("SELECT * FROM schemes WHERE category IN ('SC','ST','OBC')")

    elif filter_type == "Minority":
        cursor.execute("SELECT * FROM schemes WHERE category='Minority'")

    elif filter_type == "Women":
        cursor.execute("SELECT * FROM schemes WHERE gender='Female'")

    elif filter_type == "Laptop":
        cursor.execute("SELECT * FROM schemes WHERE scheme_name LIKE '%Laptop%' OR scheme_name LIKE '%Digital%'")

    elif filter_type == "Research":
        cursor.execute("SELECT * FROM schemes WHERE education_level='PhD'")

    else:
        cursor.execute("SELECT * FROM schemes")

    schemes = cursor.fetchall()

    # DASHBOARD STATISTICS

    cursor.execute("SELECT COUNT(*) as total FROM schemes")
    total_schemes = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as ug_count FROM schemes WHERE education_level='UG'")
    ug_count = cursor.fetchone()['ug_count']

    cursor.execute("SELECT COUNT(*) as pg_count FROM schemes WHERE education_level='PG'")
    pg_count = cursor.fetchone()['pg_count']

    cursor.execute("SELECT COUNT(*) as pwd_count FROM schemes WHERE disability='Yes'")
    pwd_count = cursor.fetchone()['pwd_count']

    cursor.execute("SELECT COUNT(*) as sports_count FROM schemes WHERE sports='Yes'")
    sports_count = cursor.fetchone()['sports_count']

    cursor.execute("SELECT COUNT(*) as caste_count FROM schemes WHERE category IN ('SC','ST','OBC')")
    caste_count = cursor.fetchone()['caste_count']

    cursor.execute("SELECT COUNT(*) as minority_count FROM schemes WHERE category='Minority'")
    minority_count = cursor.fetchone()['minority_count']

    cursor.execute("SELECT COUNT(*) as women_count FROM schemes WHERE gender='Female'")
    women_count = cursor.fetchone()['women_count']

    cursor.execute("SELECT COUNT(*) as laptop_count FROM schemes WHERE scheme_name LIKE '%Laptop%' OR scheme_name LIKE '%Digital%'")
    laptop_count = cursor.fetchone()['laptop_count']

    cursor.execute("SELECT COUNT(*) as research_count FROM schemes WHERE education_level='PhD'")
    research_count = cursor.fetchone()['research_count']

    return render_template(
        "admin_dashboard.html",
        schemes=schemes,
        total_schemes=total_schemes,
        ug_count=ug_count,
        pg_count=pg_count,
        pwd_count=pwd_count,
        sports_count=sports_count,
        caste_count=caste_count,
        minority_count=minority_count,
        women_count=women_count,
        laptop_count=laptop_count,
        research_count=research_count
    )


# LOGOUT
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return render_template("logout.html")


# VIEW ALL SCHEMES
@app.route('/schemes')
def all_schemes():

    search = request.args.get('search')

    cursor = db.cursor(dictionary=True)

    if search:
        query = "SELECT * FROM schemes WHERE scheme_name LIKE %s"
        cursor.execute(query, ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM schemes ORDER BY scheme_name")

    schemes = cursor.fetchall()

    return render_template("all_schemes.html", schemes=schemes)


# VIEW SINGLE SCHEME
@app.route('/scheme/<int:id>')
def scheme_detail(id):

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schemes WHERE id = %s", (id,))
    scheme = cursor.fetchone()

    return render_template("scheme_detail.html", scheme=scheme)


# ADD SCHEME PAGE
@app.route('/add-scheme')
def add_scheme():

    if 'admin_logged_in' not in session:
        return redirect(url_for('admin'))

    return render_template("add_scheme.html")


# DELETE SCHEME
@app.route('/delete-scheme/<int:id>')
def delete_scheme(id):

    if 'admin_logged_in' not in session:
        return redirect(url_for('admin'))

    cursor = db.cursor()
    cursor.execute("DELETE FROM schemes WHERE id=%s", (id,))
    db.commit()

    flash("Scheme deleted successfully.", "info")
    return redirect(url_for('admin_dashboard'))


# EDIT SCHEME PAGE
@app.route('/edit-scheme/<int:id>')
def edit_scheme(id):

    if 'admin_logged_in' not in session:
        return redirect(url_for('admin'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schemes WHERE id=%s", (id,))
    scheme = cursor.fetchone()

    return render_template("edit_scheme.html", scheme=scheme)


# UPDATE SCHEME
@app.route('/update-scheme/<int:id>', methods=['POST'])
def update_scheme(id):

    if 'admin_logged_in' not in session:
        return redirect(url_for('admin'))

    scheme_name = request.form['scheme_name']
    education = request.form['education']
    max_income = int(request.form['max_income'])
    category = request.form['category']
    gender = request.form['gender']
    disability = request.form['disability']
    first_graduate = request.form['first_graduate']
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
        first_graduate=%s,
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
        gender, disability, first_graduate,
        min_age, max_age,
        benefits, documents,
        official_link, youtube_link,
        id
    ))

    db.commit()

    flash("Scheme updated successfully!", "success")
    return redirect(url_for('admin_dashboard'))


# SAVE NEW SCHEME
@app.route('/save-scheme', methods=['POST'])
def save_scheme():

    if 'admin_logged_in' not in session:
        return redirect(url_for('admin'))

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
    first_graduate = request.form['first_graduate']
    official_link = request.form['official_link']
    youtube_link = request.form['youtube_link']

    cursor = db.cursor()

    query = """
    INSERT INTO schemes
    (scheme_name, education_level, max_income, category, gender,
    min_age, max_age, benefits, documents, disability,
    first_graduate, official_link, youtube_link)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (
        scheme_name, education, max_income,
        category, gender,
        min_age, max_age,
        benefits, documents,
        disability, first_graduate,
        official_link, youtube_link
    ))

    db.commit()

    flash("New scheme added successfully!", "success")
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, session, render_template, flash, redirect, url_for
from common import dbHandle
app = Flask(__name__, template_folder='template/')
app.secret_key = "$#B_SCI_SOLUTION$$#$"

@app.route('/')
@app.route('/home')
def home():
    if session.get('teacher_logged_in'):
        return redirect(url_for('login'))

    return render_template('index.html')


@app.route('/login',  methods=["POST", "GET"])
def login():
    if request.method == "POST":
        form_data = request.form.to_dict()
        email = form_data['email']
        passwd = form_data['pass']
        if passwd == '' and email == '':
            flash("Enter your Email and Password")
            return render_template('Login.html')
        elif email == '':
            flash("Enter your Email")
            return render_template('Login.html')
        elif passwd == '':
            flash("Enter your password")
            return render_template('Login.html')
        success = dbHandle.login(email, passwd)
        if success == -1:
            flash("email-id not found please register!")
        elif success == 1:
            session['logged_in'] = email
            return redirect(url_for('dashboard'))
        elif success == 0:
            flash("Password incorrect, Retry!")
    return render_template('Login.html')


@app.route('/signUp',  methods=["POST", "GET"])
def signUp():
    if 'logged_in' in session:
        render_template()
    if request.method == "POST":
        form_data = request.form.to_dict()
        print(form_data)
        fname = form_data['first_name']
        lname = form_data['last_name']
        email = form_data['email']
        passwd = form_data['Password']
        date_time = form_data['birthday']
        college_name = form_data['college_name']
        grad_year = form_data['grad_year']
        date_time_dict={}
        if date_time:
            date_time_dict = {'date': date_time[0:2], 'month': date_time[3:5], 'year': date_time[6:], 'hour':"00", 'min':"00"}

        passwdchk = form_data['Confirm Password']
        if fname == '':
            flash("Please enter your first name")
            return render_template('Sign up.html')
        elif lname == '':
            flash("Please enter last name")
            return render_template('Sign up.html')
        elif email == '':
            flash("Please enter your email")
            return render_template('Sign up.html')
        elif passwd == '':
            flash("Please enter a password")
            return render_template('Sign up.html')
        elif passwdchk == '':
            flash("Please enter confirm password")
            return render_template('Sign up.html')
        elif passwd != passwdchk:
            flash("Password and confirm password do not match, Please re-enter")
            return render_template('Sign up.html')

        print(college_name, grad_year)
        success = dbHandle.registration(fname, lname, email, passwd, date_time_dict, college_name, grad_year)
        if success == 0:
            flash("email already exists, please login")
            return render_template('Sign up.html')
        elif success == 1:
            flash("Registration Successful, Please Login")
            return redirect(url_for('login'))

    return render_template('Sign up.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        fname, lname = dbHandle.fetch_name(session['logged_in'])
        college_name, grad_year = dbHandle.fetch_college_details(session['logged_in'])

        return render_template('dashboard.html', email=session.get('logged_in'), fname = fname, lname=lname,
                               college_name= college_name, grad_year= grad_year)


@app.route('/notifications')
def notifications():
    projects = dbHandle.fetch_project(session['logged_in'])
    return render_template('notifications.html', lp = len(projects), projects=projects)


@app.route('/table')
def table():
    projects = dbHandle.fetch_project(session['logged_in'])
    return render_template('table.html', lp = len(projects), projects=projects)


@app.route('/project_Add', methods=["POST", "GET"])
def project_Add():
    if request.method == "POST":
        form_data = request.form.to_dict()
        print(form_data)
        name = form_data['name']
        field = form_data['field']
        emails = [form_data['email1'], form_data['email2'], form_data['email3'], form_data['email4']]
        emails = list(filter(None, emails))
        about = form_data['about']
        dbHandle.createProject(emails, name, field, about)

    return render_template('project_Add.html')


@app.route('/user', methods=["POST", "GET"])
def user():
    if session.get('logged_in'):
        fname,lname = dbHandle.fetch_name(session['logged_in'])
        college_name,grad_year = dbHandle.fetch_college_details(session['logged_in'])
        if request.method == "POST":
            form_data = request.form.to_dict()
            fname = form_data['fname']
            lname = form_data['lname']
            email = session['logged_in']
            college_name = form_data['college_name']
            grad_year = form_data['grad_year']
            dbHandle.update_details(fname, lname, email, college_name, grad_year)
        return render_template('user.html', email=session.get('logged_in'), fname = fname, lname= lname, college_name=college_name, grad_year= grad_year)


@app.route('/logout')
def logout():
    session.pop('logged_in')
    flash("Thanks for visiting our site..! \nLogged out successfully ")
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug="true")

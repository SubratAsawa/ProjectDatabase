import pymysql
import bcrypt

def connect():
    try:
        mydb = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            database='project_database',
        )
    except:
        connect()
    return mydb


def login(emailid: str, passwd: str):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT pass from login where email = \"" + emailid + "\"")
    fetched_list = mycursor.fetchall()
    if (len(fetched_list) == 0):
        return -1  # email id not found

    else:
        hassedPasswd = fetched_list[0][0]
        if bcrypt.checkpw(passwd.encode("utf-8"), hassedPasswd.encode("utf-8")):
            return 1  # login success
        else:
            return 0  # incorrect password


def registration(fname: str, lname:str, email: str, passwd: str, date_time: dict, college_name: str, grad_year):
    mydb = connect()
    mycursor = mydb.cursor()
    hassedPasswd = bcrypt.hashpw(passwd.encode("utf-8"), bcrypt.gensalt())

    insertFn = "INSERT INTO login (fname, lname, email, pass, college, grad_year) VALUES (%s, %s, %s, %s, %s, %s)"
    registration_info = (fname, lname, email, hassedPasswd, college_name, grad_year)
    mycursor.execute (insertFn, registration_info)
    mydb.commit()

    return 1


def fetch_name(email:str):
    mydb = connect ()
    mycursor = mydb.cursor ()

    mycursor.execute ("SELECT fname,lname from login where email=\"" + email + "\"")
    fetched_list = mycursor.fetchall ()
    return fetched_list[0][0],fetched_list[0][1]


def createProject(emails: list, project_name:str, field: str, about: str):
    mydb = connect()
    mycursor = mydb.cursor()

    insertFn = "INSERT INTO projects (name, field, about) VALUES (%s, %s, %s)"
    info = (project_name, field, about)
    mycursor.execute(insertFn, info)
    mydb.commit()
    mapping(emails)
    return 1


def mapping(emails: list):
    mydb = connect()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT MAX(id) FROM projects")
    pid = mycursor.fetchall()[0][0]
    for email in emails:
        insertFn = "INSERT INTO map (pid, email) VALUES (%s, %s)"
        mapping_info = (pid, email)
        mycursor.execute(insertFn, mapping_info)
        mydb.commit()
    return 1


def fetch_project(email:str):
    mydb = connect()
    mycursor = mydb.cursor()
    project_list = []
    mycursor.execute("SELECT pid from map where email = \"" + email + "\"")
    fetched_list = mycursor.fetchall()
    le = len(fetched_list)
    if le == 0:
        return project_list  # no products register
    else:
        for i in range(le):
            mycursor.execute("select * from projects where id = " + str(fetched_list[i][0]))
            p_list = mycursor.fetchall()

            tempDict = {"pid": p_list[0][0],
                        "name": p_list[0][1],
                        "field": p_list[0][2],
                        "about": p_list[0][3]}
            project_list.append(tempDict)

        return project_list


def fetch_college_details(email: str):
    mydb = connect()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT college,grad_year from login where email=\"" + email + "\"")
    fetched_list = mycursor.fetchall()
    return fetched_list[0][0], fetched_list[0][1]


def update_details(fname,lname, email, college_name, grad_year):
    mydb = connect()
    mycursor = mydb.cursor()

    sql_str = f"UPDATE login SET fname = \"{fname}\", lname = \"{lname}\", email=\"{email}\", college=\"{college_name}\", grad_year=\"{grad_year}\" where email = \"{email}\""
    mycursor.execute(sql_str)
    mydb.commit()
    return 1

def fetch_all_emails():
    mydb = connect()
    mycursor = mydb.cursor()

    mycursor.execute("SELECT email from login")
    fetched_list = mycursor.fetchall()
    return fetched_list

for i in fetch_all_emails():
    print(i[0])

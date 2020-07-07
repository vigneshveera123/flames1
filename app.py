from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypass'
app.config['MYSQL_DB'] = 'flames_db'

mysql = MySQL(app)


# flamesweb_page
@app.route('/flames')
def flames():
    return render_template("flames.html")


# index_web_page
@app.route('/index', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        details = request.form
        first_name = details['your_name']
        last_name = details['couple_name']
        c = set(first_name.lower().replace(' ', ''))
        d = set(last_name.lower().replace(' ', ''))
        c.intersection_update(d)
        g = len(c)
        re = get_result(g)
        cur= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        this_query = "insert into logs (name_one,name_two,result) values ('" + first_name + "','" + last_name + "','" + re + "')"
        que="select * from logs"
        cur.execute(que)
        table=cur.fetchall()
        cur.execute(this_query)
        mysql.connection.commit()
        cur.close()
        return render_template('index.html', name=re)


# flames_medots
def get_result(g):
    if g in [5, 14, 16, 18, 21, 23]:
        return "FRIENDS"
    elif g in [3, 10, 19]:
        return "LOVER"
    elif g in [8, 12, 13, 17]:
        return "Affection"
    elif g in [6, 11, 15, 26]:
        return "MARRIAGE"
    elif g in [2, 4, 7, 9, 20, 22, 24, 25]:
        return "ENEMY"
    else:
        return "SIBLINGS"


# login_page
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        details = request.form
        user_name = details['user_name']
        password = details['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM login_table WHERE user_name = '"+user_name+"'  AND password = '"+password+"' ")
        # Fetch one record and return result
        account = cur.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['logged_in'] = True
            session['id'] = account['id']
            session['user_name'] = account['user_name']
            # Redirect to home page
            return redirect(url_for('admin'))
        else:
            # Account doesnt exist or username/password incorrect
            return redirect(url_for('newlogin'))
    else:
        return render_template("login.html")


@app.route("/newlogin",methods=["POST","GET"])
def newlogin():
    if request.method == "POST":
        details = request.form
        user_name = details['user_name']
        password = details['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        this_query = "insert into login_table (user_name,password) values (%s,%s)"
        cur.execute(this_query,[user_name,password])
        mysql.connection.commit()
        cur.close()
        return redirect('login')

    return render_template("newlogin.html")


@app.route('/admin',methods=["POST","GET"])
def admin():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM logs")
    # Fetch one record and return result
    info = cur.fetchall()
    if session.get('logged_in'):
        return render_template("admin.html",tables=info)
    else:
        return redirect(url_for('login'))


@app.route('/edit/<string:id>',methods=["POST","GET"])
def edit(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == "POST":
        details = request.form
        first_name = details['your_name']
        last_name = details['couple_name']
        re = details['result']
        this_query = "update logs set name_one=%s,name_two=%s,result=%s where log_id=%s"
        cur.execute(this_query,[first_name,last_name,re,id])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("admin"))
        cur = mysql.connection.cursor()

    qeu="select * from logs where log_id=%s"
    cur.execute(qeu,[id])
    res=cur.fetchone()
    return render_template("edit.html",datas=res)

@app.route('/delete/<string:id>',methods=["POST","GET"])
def delete(id):
    cur = mysql.connection.cursor()
    sql="delete from logs where log_id=%s"
    cur.execute(sql,[id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("admin"))



if __name__ == "__main__":
    app.debug = True
    app.run()

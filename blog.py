# Team Joe
#
# SoftDev1 pd09
# P#00 Da Art of Storytellin'
# 2019-10-28

from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os

#-----------------------------------------------------------------
#DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='userdata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE userdata (user TEXT, pass TEXT);")
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='blogdata' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE blogdata(user TEXT,blogid INT, title TEXT,content BLOB);")

#-----------------------------------------------------------------
#FLASK APP

app = Flask(__name__)
app.secret_key = os.urandom(32)
message = ""
loggedin = False

def rend_temp(template, mess):
    global message
    if (mess != ""):
        message = ""
        return render_template(template, m = mess)
    return render_template(template)

@app.route("/", methods=['GET', 'POST'])
def Login():
    with sqlite3.connect("info.db") as db:
        c = db.cursor()
        c.execute("SELECT * FROM userdata")
        valid = c.fetchall()
    if("username" in session and "password" in session):
        if (session["username"], session["password"]) in valid:
            return redirect("/Main")
    return render_template("LoginPage.html")

##check if the user entered a valid combo of username and passwor
@app.route("/loginhelper", methods=['GET', 'POST'])
def helper():
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        c.execute("SELECT * FROM userdata")
        valid = c.fetchall()
        if (request.args["username"], request.args["password"]) in valid:
            session["username"] = request.args["username"]
            session["password"] = request.args["password"]
            return redirect("/Main")
        if (session["username"], session["password"]) in valid:
            return redirect("/Main")
        return redirect("/")


@app.route("/Main")
def Main():
    with sqlite3.connect("info.db") as db:
        c = db.cursor()
        c.execute("SELECT * FROM blogdata")
        allblogs = c.fetchall()
        return render_template("MainPage.html",smth = allblogs)

@app.route("/Register", methods=['GET', 'POST'])
def Register():
    return rend_temp("RegisterPage.html", message)


##Below is a checker
##If you register, it checs the following
@app.route("/Registered", methods= ['GET', 'POST'])
def Registered():
    global message
    with sqlite3.connect(DB_FILE) as db:
        if (len(request.args["username"]) > 0):
            c = db.cursor()
            c.execute('SELECT * FROM userdata WHERE user = (?)', (request.args["username"],))
            if (len(c.fetchall()) > 0) :
                message = "Username already exists."
                return redirect("/Register")
            if (len(request.args["password"]) == 0):
                message = "Password is empty."
                return redirect("/Register")
            if (request.args["password"] == request.args["repeat"]):
                c.execute('INSERT INTO userdata VALUES (?, ?)',(request.args["username"], request.args["password"]))
                message = "Account Created!"
                return redirect("/")
            else:
                message = "Passwords do not match."
                return redirect("/Register")
        message = "Username not filled out."
        return redirect("/Register")
        # c = db.cursor()
        # if (request.args["password"] == request.args["repeat"]):
        #     #first, if u repeat ur passwoard
        #     if type(c.fetchone()) is None:
        #         #(if there are no accounts itll make a table)
        #         c.execute("CREATE TABLE userdata (user TEXT, pass TEXT);")
        #     #otherwise itll add ur username and password to the database for you to login
        #     c.execute('INSERT INTO userdata VALUES (?, ?)',(request.args["username"], request.args["password"]))
        #     return redirect("/")
        #     #then you go back to the login page
        # #if you didnt return, that means you didnt have equal passwords
        # #so the following will help show that
        # return redirect("/Register")




@app.route("/Profile")
def Profile():
	return render_template("ProfilePage.html")

@app.route("/CreateBlog")
def CreateBlog():
	return render_template("CreateBlogPage.html")

@app.route("/MyBlogs")
def MyBlogs():
	    return render_template("MyBlogsPage.html")


command = "SELECT * FROM userdata"          # test SQL stmt in sqlite3 shell, save as string
c.execute(command)
#print(555555555555555555554444444444)
print(c.fetchall())
#print(44444444445555555555555)
db.commit()
db.close()

if __name__ == "__main__":
	app.debug = True
	app.run()

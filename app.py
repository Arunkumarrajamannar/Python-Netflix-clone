from flask import Flask,render_template,request,session,url_for,redirect
import sqlite3 as sql
from pytube import extract

app = Flask(__name__)
app.secret_key = "Arun123"
login_pin = "2487"

def isloggedin():
    return "email" in session

@app.route('/', methods = ["GET","POST"])
def login():
    if request.method == "POST":

        email1 = request.form.get("email1")
        password1 = request.form.get("password1")
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("select * from netflix where email=? and password=?",(email1,password1))
        fet = cur.fetchall()
        for i in fet:
            if email1 in i and  password1 == i[3]:
                session["email"] = email1
                return redirect (url_for('pin'))
            else:
                return "Incorrect username or password"
    return render_template ("login.html")

@app.route('/signup', methods = ["GET","POST"])
def signup():
    if request.method =="POST":
        username = request.form.get("username")
        dob = request.form.get("dob")
        email = request.form.get("email")
        password = request.form.get("password")

        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("insert into netflix (username,dob,email,password) values(?,?,?,?)",
                    (username,dob,email,password))
        con.commit()
        return redirect (url_for('login'))
    
    return render_template ("signup.html")



@app.route('/netflix')
def netflix():
    con = sql.connect("user.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from upload")
    fet = cur.fetchall()
    return render_template ("netflix.html", box = fet)

@app.route('/playingmovie/<var>')
def movies(var):
    return render_template("movies.html",VAR = var)

@app.route('/upload', methods = ["GET","POST"])
def search():
    if request.method == "POST":
        video = request.form.get("video")
        videoid = extract.video_id(video)
        thumb = request.form.get("thumb")
        con = sql.connect("user.db")
        cur = con.cursor()
        cur.execute("insert into upload (videourl,thumburl) values(?,?)",
                    (videoid,thumb))
        con.commit()
        return redirect (url_for('netflix'))

    return render_template ("search.html")



@app.route('/is that you')
def watch():
    return render_template ("watch.html")

@app.route('/pin', methods = ["GET","POST"])
def pin():
    if request.method == "POST":
        pin = request.form.get("pin")
        if pin == login_pin:
            return  redirect (url_for('watch'))
        else:
            return "Try Again"
    return render_template ("pin.html")





if __name__ == "__main__":
    app.run(debug=True)


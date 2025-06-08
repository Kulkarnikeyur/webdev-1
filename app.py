from flask import Flask,render_template,request,flash,session,redirect
import mysql.connector
import os
from random import *
app = Flask(__name__)

mydb = mysql.connector.connect(
    host='brh51esi52fw7ncryz7o-mysql.services.clever-cloud.com',
    user='ujofuri1anddaopg',
    password='Vfg5VhW6X7Scb4tIoiCq',
    database='brh51esi52fw7ncryz7o',
    port=3306
)
app.secret_key="kkeyur"

@app.route("/")
def hello():
    return render_template("main.html")

@app.route("/name")
def n():
    return render_template("name.html")

@app.route("/start",methods=["post"])
def start():
    session["random"]=randint(1,100)
    session["moves"]=0
    session["name"]=request.form["name"]
    return redirect("/game")

@app.route("/game")
def g():
    return render_template("game.html")

@app.route("/score",methods=["post"])
def score():
    if(request.form["number"]==""):
        flash("enter a valid number")
        return redirect("/game")
    number=int(request.form["number"])
    if(number==session["random"]):
        session["moves"]+=1
        return redirect("/congrats")
    elif(number>session["random"]):
        session["moves"]+=1
        flash("too high!")
        return redirect("/game")
    else:
        session["moves"]+=1
        flash("too low!")
        return redirect("/game")

@app.route("/congrats")
def c():
    cursor = mydb.cursor()
    sql="insert into store (name,rand,score) values(%s,%s,%s)"
    values=(session.get("name"),session.get("random"),session.get("moves"))
    cursor.execute(sql,values)

    mydb.commit()

    cursor.close()
    mydb.close()

    return render_template("congrats.html",name=session.get("name"),score=session.get("moves"))

@app.route("/replay")
def replay():
    session["moves"]=0
    session["random"]=randint(1,100)
    return redirect("/game")

@app.route("/history")
def history():
    cursor = mydb.cursor()
    cursor.execute("SELECT name, rand, score FROM store ORDER BY score ASC")
    data = cursor.fetchall()  # returns a list of tuples

    cursor.close()
    mydb.close()
    return render_template("history.html", data=data)

if __name__ == "__main__":
    app.run()

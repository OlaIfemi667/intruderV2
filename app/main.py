from flask import Flask, render_template
from core.modules.database import *

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")


@app.route("/home/outils")
def showUtils():
    return render_template("utils.html")

@app.route("/home/outils/<utilName>")
def showUtilsDetail(utilName):
    return render_template("utilsDetails.html", utilName=utilName)

@app.route("/home/profiler")
def showProfiler():
    return render_template("profiler.html")


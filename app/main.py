from flask import Flask, render_template, request
from core.modules.database import *
from core.modules.scanner import *
from sublister.sublist3r import *
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("home.html")


@app.route("/home/outils")
def showUtils():
    return render_template("utils.html")

@app.route("/home/outils/<utilName>", methods=["POST", "GET"])
def showUtilsDetail(utilName):
    if request.method == "POST":
        if utilName == "networkscanner": 
            out = portScanner(request.form["ip"], "22-80")
            addScannerOutput("netRecon", out)
            return render_template("utilsDetails.html", utilName=utilName, output = out)
        elif utilName == "sublist3r": 
            passsubdomains = sublisterMain(request.form["domain"], 40, f"../text/{request.form["domain"]}.txt", ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
            addScannerOutput("sublister", str(passsubdomains))
            return render_template("utilsDetails.html", utilName=utilName, output = passsubdomains)
    else:
        return render_template("utilsDetails.html", utilName=utilName)

@app.route("/home/profiler")
def showProfiler():
    return render_template("profiler.html")


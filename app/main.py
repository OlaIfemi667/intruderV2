from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1/outils")
def showAllScanType():
    return "<p>Types de scans</p>"

@app.route("/api/v1/outils/<utilName>")
def showScanType(scannerName):
    return f"<p>Type de scan : {scannerName}</p>"


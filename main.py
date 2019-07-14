from flask import Flask, render_template, request     
from mapColoring.colorAssignment import colorAssignment
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/color", methods = ["GET"])
def color():
	continent = request.args["continent"]
	nColors = request.args["nColors"]
	ca = colorAssignment(continent)
	ca.formatInput(nColors)
	return ca.runModule()

if __name__ == "__main__":
    app.run(debug=True)
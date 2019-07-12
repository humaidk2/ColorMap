from flask import Flask, render_template, request     
from mapColoring.colorAssignment import colorAssignment
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/color")
def color():
	ca = colorAssignment()
	ca.formatInput()
	return {"finalOutput": ca.runModule()}

if __name__ == "__main__":
    app.run(debug=True)
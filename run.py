import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)
import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Nutrition Value App</h1>"


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)
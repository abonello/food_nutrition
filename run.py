import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    foodItem2 = {
        "name": "Capers", 
        "brand": "Fragata", 
        "energy1": "111.kJ", 
        "energy2": "27.kcal", 
        "fat": "0.2g", 
        "saturated": "0.2g", 
        "carbohydrates": "2.2g", 
        "sugar": "2.2g", 
        "fibre": "NA", 
        "protein": "0.8g", 
        "salt": "6.7g",
        "classification": "Capers", 
        "shop": "Tesco", 
        "notes": "in vinegar / info as dried"}


# Sundried Tomatoes,Tesco,674.kJ,163.kcal,,11.9g,,1.4g,,7.0g,6.4g,,7.9g,3.0g,2.8g,NA,NA,Dried Tomatoes,Tesco,Marinated with garlic in sunflower oil and virgin olive oil / drained

    return render_template("index.html", food=foodItem2)


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)
import os
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    foodItems = [
        {
             "name": "Tomato Puree",
             "brand": "Cucina",
             "energy1": "335.kJ",
             "energy2": "79.kcal",
             "fat": "0.5g",
             "saturated": "0.1g",
             "carbohydrates": "14.0g",
             "sugar": "14.0g",
             "fibre": "1.8g",
             "protein": "4.3g",
             "salt": "1.6g",
             "classification": "Tomato Puree",
             "shop": "Aldi",
             "notes": "Double Concentrate / 20g = 1/5-a-day"
        },
        {
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
            "notes": "in vinegar / info as dried"
        },
        {
            "name": "Sundried Tomatoes",
            "brand": "Tesco",
            "energy1": "674.kJ",
            "energy2": "163.kcal",
            "fat": "11.9g",
            "saturated": "1.4g",
            "carbohydrates": "7.0g",
            "sugar": "6.4g",
            "fibre": "7.9",
            "protein": "3.0g",
            "salt": "2.8g",
            "classification": "Dried Tomatoes",
            "shop": "Tesco",
            "notes": "Marinated with garlic in sunflower oil and virgin olive oil / drained"
        }
    ]
    


# Sundried Tomatoes,Tesco,674.kJ,163.kcal,,11.9g,,1.4g,,7.0g,6.4g,,7.9g,3.0g,2.8g,NA,NA,Dried Tomatoes,Tesco,Marinated with garlic in sunflower oil and virgin olive oil / drained

    return render_template("index.html", food=foodItems)


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)
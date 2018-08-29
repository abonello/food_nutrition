import os
from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from connection import getDbName, getURI  # Needed to run locally - Comment out for heroku


app = Flask(__name__)
# Use the following to run LOCALLY will need the import
app.config["MONGO_DBNAME"] = getDbName()
app.config["MONGO_URI"] = getURI()

# Use the following to run from HEROKU - remove the import
# app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
# app.config["MONGO_URI"] = os.getenv('MONGO_URI')


# collection = getCollection()
# FIELDS = {
#             'name': True, 
#             'brand': True, 
#             'energy1': True, 
#             'energy2': True, 
#             'fat': True, 
#             'saturated': True, 
#             'carbohydrates': True,
#             'sugar': True, 
#             'fibre': True, 
#             'protein': True, 
#             'salt': True,
#             'classification': True, 
#             'shop': True, 
#             'notes': True, 
#             '_id': False
#         }


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_food_items")
def get_food_items():
    # foodItems = [
    #     {
    #          "name": "Tomato Puree",
    #          "brand": "Cucina",
    #          "energy1": "335.kJ",
    #          "energy2": "79.kcal",
    #          "fat": "0.5g",
    #          "saturated": "0.1g",
    #          "carbohydrates": "14.0g",
    #          "sugar": "14.0g",
    #          "fibre": "1.8g",
    #          "protein": "4.3g",
    #          "salt": "1.6g",
    #          "classification": "Tomato Puree",
    #          "shop": "Aldi",
    #          "notes": "Double Concentrate / 20g = 1/5-a-day"
    #     },
    #     {
    #         "name": "Capers",
    #         "brand": "Fragata",
    #         "energy1": "111.kJ",
    #         "energy2": "27.kcal",
    #         "fat": "0.2g",
    #         "saturated": "0.2g",
    #         "carbohydrates": "2.2g",
    #         "sugar": "2.2g",
    #         "fibre": "NA",
    #         "protein": "0.8g",
    #         "salt": "6.7g",
    #         "classification": "Capers",
    #         "shop": "Tesco",
    #         "notes": "in vinegar / info as dried"
    #     },
    #     {
    #         "name": "Sundried Tomatoes",
    #         "brand": "Tesco",
    #         "energy1": "674.kJ",
    #         "energy2": "163.kcal",
    #         "fat": "11.9g",
    #         "saturated": "1.4g",
    #         "carbohydrates": "7.0g",
    #         "sugar": "6.4g",
    #         "fibre": "7.9",
    #         "protein": "3.0g",
    #         "salt": "2.8g",
    #         "classification": "Dried Tomatoes",
    #         "shop": "Tesco",
    #         "notes": "Marinated with garlic in sunflower oil and virgin olive oil / drained"
    #     }
    # ]
    

# Sundried Tomatoes,Tesco,674.kJ,163.kcal,,11.9g,,1.4g,,7.0g,6.4g,,7.9g,3.0g,2.8g,NA,NA,Dried Tomatoes,Tesco,Marinated with garlic in sunflower oil and virgin olive oil / drained

    # return render_template("index.html", food=foodItems)
    return render_template("index.html", food=mongo.db.nutrition100.find())


@app.route("/add_food_item")
def add_food_item():
    return render_template("addfooditem.html", classification=mongo.db.classification.find())
    # return render_template("addfooditem.html", classification=mongo.db.classification.find(), cameFrom="add_food_item")


@app.route("/insert_food_item", methods=["POST"])
def insert_food_item():
    foods = mongo.db.nutrition100
    data = request.form.to_dict()
    data["energy1"] = data["energy1"] + "kJ"
    data["energy2"] = data["energy2"] + "kcal"
    data["fat"] = data["fat"] + "g"
    data["saturated"] = data["saturated"] + "g"
    data["carbohydrates"] = data["carbohydrates"] + "g"
    data["sugar"] = data["sugar"] + "g"
    data["fibre"] = data["fibre"] + "g"
    data["protein"] = data["protein"] + "g"
    data["salt"] = data["salt"] + "g"
    del data["action"]
    foods.insert_one(data)
    return redirect(url_for("get_food_items"))

@app.route("/delete_food_item/<food_item_id>")
def delete_food_item(food_item_id):
    mongo.db.nutrition100.remove({"_id": ObjectId(food_item_id)})
    return redirect(url_for('get_food_items'))



#-------------FOOD CLASSES-----------------------------
@app.route("/get_classification")
def get_classification():
    return render_template("classification.html", classification=mongo.db.classification.find())
    # return render_template("classification.html", classification=mongo.db.classification.find(), cameFrom="get_classification")

@app.route("/delete_class/<class_id>")
def delete_class(class_id):
    mongo.db.classification.remove({"_id": ObjectId(class_id)})
    return redirect(url_for('get_classification'))

@app.route("/add_class/<cameFrom>")
@app.route("/add_class")
def add_class(cameFrom=""): # I want to check that class does not exist
    return render_template("addclass.html", classification=mongo.db.classification.find(), cameFrom=cameFrom)
    # return render_template("addcategory.html")


@app.route("/insert_class", methods=['POST'])
def insert_class():
    classification = mongo.db.classification
    data = request.form.to_dict()
    del data["action"]
    # classification.find().forEach(function(e) { print(e)})
    for food_class in classification.find():
        # print(food_class['class'])
        if data['class'].lower() == food_class['class'].lower():
            return render_template("addclass.html", classification=mongo.db.classification.find(), entry=data['class'])
        else:
            data['class'] = data['class'].capitalize()
            classification.insert_one(data)
            return redirect(url_for("get_classification"))


if __name__ == '__main__':
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)
    app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True) # Is it because of the different server?
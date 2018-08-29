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


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_food_items")
def get_food_items():
    return render_template("index.html", food=mongo.db.nutrition100.find())


@app.route("/add_food_item")
def add_food_item():
    return render_template("addfooditem.html", classification=mongo.db.classification.find())


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


@app.route("/edit_food_item/<food_item_id>")
def edit_food_item(food_item_id):
    food_item = mongo.db.nutrition100.find_one({"_id": ObjectId(food_item_id)})
    return render_template("editfooditem.html", foodItem=food_item, classification=mongo.db.classification.find())
    
    
@app.route("/update_food_item/<food_item_id>", methods=["POST"])
def update_food_item(food_item_id):
    nutrition100 = mongo.db.nutrition100
    data = request.form.to_dict()
    del data["action"]
    nutrition100.update({"_id": ObjectId(food_item_id)}, data)
    return redirect(url_for('get_food_items'))




#-------------FOOD CLASSES-----------------------------
@app.route("/get_classification")
def get_classification():
    return render_template("classification.html", classification=mongo.db.classification.find())


@app.route("/delete_class/<class_id>")
def delete_class(class_id):
    mongo.db.classification.remove({"_id": ObjectId(class_id)})
    return redirect(url_for('get_classification'))


@app.route("/add_class/<cameFrom>")
@app.route("/add_class")
def add_class(cameFrom=""): # I want to check that class does not exist
    return render_template("addclass.html", classification=mongo.db.classification.find(), cameFrom=cameFrom)


@app.route("/insert_class", methods=['POST'])
def insert_class():
    classification = mongo.db.classification
    data = request.form.to_dict()
    del data["action"]
    for food_class in classification.find():
        print(food_class['class'])
        if data['class'].lower() == food_class['class'].lower():
            print("There is a match")
            return render_template("addclass.html", classification=mongo.db.classification.find(), entry=data['class'])

    data['class'] = data['class'].capitalize()
    classification.insert_one(data)
    return redirect(url_for("get_classification"))


@app.route('/edit_class/<class_id>')
def edit_class(class_id):
    return render_template('editclass.html', foodClass=mongo.db.classification.find_one({'_id': ObjectId(class_id)}))
    

@app.route('/update_class/<class_id>', methods=['POST'])
def update_class(class_id):
    classification = mongo.db.classification
    data = request.form.to_dict()
    del data["action"]
    classification.update({"_id": ObjectId(class_id)}, data)
    return redirect(url_for('get_classification'))


if __name__ == '__main__':
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)
    app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True) # Is it because of the different server?
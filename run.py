import os
from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_mail import Mail, Message

# from connection import getDbName, getURI  # Needed to run locally - Comment out for heroku


app = Flask(__name__)
    # Use the following to run LOCALLY will need the import
app.config.from_pyfile('config.cfg')

    # Use the following to run from HEROKU - remove the import
# app.config["MONGO_DBNAME"] = os.getenv('MONGO_DBNAME')
# app.config["MONGO_URI"] = os.getenv('MONGO_URI')
# app.config["MAIL_SERVER"] = os.getenv('MAIL_SERVER')
# app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
# app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
# app.config["MAIL_PORT"] = os.getenv('MAIL_PORT')
# app.config["MAIL_USE_SSL"] = os.getenv('MAIL_USE_SSL')
# app.config["MAIL_DEFAULT_SENDER"] = os.getenv('MAIL_DEFAULT_SENDER')


mongo = PyMongo(app)
mail = Mail(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_food_items")
def get_food_items():
    return render_template("fooditems.html", food=mongo.db.nutrition100.find())


@app.route("/add_food_item")
def add_food_item():
    return render_template("addfooditem.html", classification=mongo.db.classification.find())


@app.route("/insert_food_item", methods=["POST"])
def insert_food_item():
    foods = mongo.db.nutrition100
    classes = mongo.db.classification
    data = request.form.to_dict()
    del data["action"]
    thisClass = classes.find_one({"class": data["classification"]})
    thisClass['count'] = str(int(thisClass['count']) + 1)
    classes.update({"class": data["classification"]}, thisClass)
    foods.insert_one(data)
    return redirect(url_for("get_food_items"))


@app.route("/confirm_delete_food_item/<food_item_id>")
def confirm_delete_food_item(food_item_id):
    foodItem = mongo.db.nutrition100.find_one({"_id": ObjectId(food_item_id)})
    return render_template("confirmdeletefooditem.html", foodItem=foodItem)


@app.route("/delete_food_item/<food_item_id>")
def delete_food_item(food_item_id):
    foodItem = mongo.db.nutrition100.find_one({"_id": ObjectId(food_item_id)})
    classes = mongo.db.classification
    targetClass = foodItem["classification"]
    thisClass = classes.find_one({"class": targetClass})
    thisClass['count'] = str(int(thisClass['count']) - 1)
    classes.update({"class": targetClass}, thisClass)
    mongo.db.nutrition100.remove({"_id": ObjectId(food_item_id)})
    return redirect(url_for('get_food_items'))


@app.route("/edit_food_item/<food_item_id>")
def edit_food_item(food_item_id):
    food_item = mongo.db.nutrition100.find_one({"_id": ObjectId(food_item_id)})
    return render_template("editfooditem.html", foodItem=food_item, classification=mongo.db.classification.find())
    
    
@app.route("/update_food_item/<food_item_id>/<oldClass>", methods=["POST"])
def update_food_item(food_item_id, oldClass):
    nutrition100 = mongo.db.nutrition100
    data = request.form.to_dict()
    del data["action"]

    if oldClass == data['classification']:
        pass # If equal: No change -> do nothing
    else:
        classes = mongo.db.classification
        thisClass = classes.find_one({"class": oldClass})
        thisClass['count'] = str(int(thisClass['count']) - 1)
        classes.update({"class": oldClass}, thisClass)
        thisClass = classes.find_one({"class": data["classification"]})
        thisClass['count'] = str(int(thisClass['count']) + 1)
        classes.update({"class": data["classification"]}, thisClass)

    nutrition100.update({"_id": ObjectId(food_item_id)}, data)
    return redirect(url_for('get_food_items'))



#-------------FOOD CLASSES-----------------------------
@app.route("/get_classification")
def get_classification():
    return render_template("classification.html", classification=mongo.db.classification.find())


@app.route("/confirm_delete_class/<class_id>")
def confirm_delete_class(class_id):
    foodType = mongo.db.classification.find_one({"_id": ObjectId(class_id)})
    return render_template("confirmdeleteclass.html", classification=foodType)


@app.route("/delete_class/<class_id>")
def delete_class(class_id):
    mongo.db.classification.remove({"_id": ObjectId(class_id)})
    return redirect(url_for('get_classification'))


@app.route("/add_class/<cameFrom>")
@app.route("/add_class")
def add_class(cameFrom=""):
    return render_template("addclass.html", classification=mongo.db.classification.find(), cameFrom=cameFrom)


@app.route("/insert_class/<cameFrom>", methods=['POST'])
def insert_class(cameFrom=""):
    classification = mongo.db.classification
    data = request.form.to_dict()
    del data["action"]

    # There must be a category name otherwise display error message.
    if data['class'] == "":
        return render_template("addclass.html", classification=mongo.db.classification.find(), cameFrom=cameFrom,  empty=True)

    for food_class in classification.find():
        if data['class'].lower() == food_class['class'].lower():
            return render_template("addclass.html", classification=mongo.db.classification.find(), cameFrom=cameFrom,  entry=data['class'])

    data['class'] = data['class'].capitalize()
    data['count'] = "0"
    classification.insert_one(data)
    if cameFrom == 'add_food_item':
        return redirect(url_for('add_food_item'))
    elif cameFrom == 'get_classification':
        return redirect(url_for('get_classification'))
    else:
        return redirect(url_for('get_classification'))


@app.route('/edit_class/<class_id>')
def edit_class(class_id):
    return render_template('editclass.html', foodClass=mongo.db.classification.find_one({'_id': ObjectId(class_id)}))
    

@app.route('/update_class/<class_id>', methods=['POST'])
def update_class(class_id):
    classification = mongo.db.classification
    data = request.form.to_dict()
    del data["action"]
    oldClassName = classification.find_one({"_id": ObjectId(class_id)})["class"]
    count = classification.find_one({"_id": ObjectId(class_id)})["count"]
    data["count"] = count
    newName = data["class"]

    # There must be a category name otherwise display error message.
    if data['class'] == "":
        return render_template("editclass.html", foodClass=mongo.db.classification.find_one({'_id': ObjectId(class_id)}),  empty=True)
    
    if oldClassName != data["class"]:
        classExist = classification.find_one({"class":newName})
        if classExist:
            if int(count) > 0:
                return render_template("confirmeditclasstoalreadyexistingname.html", class_id=class_id, data=data)

            classification.remove({"_id": ObjectId(class_id)})
            return redirect(url_for('get_classification'))

        else:
            nutrition100 = mongo.db.nutrition100
            foodItemsUsingThisClass = list(nutrition100.find({"classification": oldClassName}))

            if int(count) > 0:
                for item in foodItemsUsingThisClass:
                    itemId = item["_id"]
                    item["classification"] = data["class"]
                    nutrition100.update({"_id": ObjectId(itemId)}, item)

    classification.update({"_id": ObjectId(class_id)}, data)
    return redirect(url_for('get_classification'))

@app.route("/proceed_editing_class/<class_id>/<data>")
def proceed_editing_class(class_id, data):
    data = json.loads(data.replace("'", '"'))
    classification = mongo.db.classification
    nutrition100 = mongo.db.nutrition100
    oldClassName = classification.find_one({"_id": ObjectId(class_id)})["class"]
    foodItemsUsingThisClass = list(nutrition100.find({"classification": oldClassName}))
    count = classification.find_one({"_id": ObjectId(class_id)})["count"]
    newName = data["class"]
    classExist = classification.find_one({"class":newName})

    for item in foodItemsUsingThisClass:
        itemId = item["_id"]
        item["classification"] = data["class"]
        nutrition100.update({"_id": ObjectId(itemId)}, item)

    newCount = str(int(classExist["count"]) + int(count))
    classExist["count"] = newCount
    classExistId = classExist["_id"]
    classification.update({"_id": ObjectId(classExistId)}, classExist)
    classification.remove({"_id": ObjectId(class_id)})
    return redirect(url_for('get_classification'))


#-------------DASHBOARD-----------------------------
@app.route("/dashboard")
def dashboard():
    foodItems=mongo.db.nutrition100.find()
    foodList = []
    for eachItem in foodItems:
        eachItem["_id"] = str(eachItem["_id"])
        foodList.append(eachItem)

    foodList = json.dumps(foodList, indent=2)
    data = {'food_list': foodList}
    return render_template("dashboard.html", data=data)


#-------------OTHERS-----------------------------
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == "GET":
        return render_template ("contact.html")
    try:
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        msg = Message(subject, sender=email, recipients=[app.config['MAIL_DEFAULT_SENDER']])
        msg.body = "{} sent the following message through the Nutrition website: \n\n{}".format(name, message)
        mail.send(msg)
        return render_template("message_sent.html", name=name, email=email, subject=subject, message=message)
    except Exception as e:
        return render_template("message_error.html", email=email)

'''
ERROR EXAMPLE:
smtplib.SMTPRecipientsRefused: {'websiteadmin@anthonybonello.co.uk': (550, b'Verification failed for <anthony@hotmail>\nThe mail server could not deliver mail to anthonybonello_music@hotmail.  The account or domain may not exist, they may be blacklisted, or missing the proper dns entries.\nSender verify failed')}'''


#-------------DATA BACKUP-----------------------------
@app.route("/get_data_backup")
def get_data_backup():
    food=mongo.db.nutrition100.find()
    classes = mongo.db.classification.find()
    nutrition100 = dumps(food)
    classification = dumps(classes)
    with open("data_backup/nutrition100.json", 'w') as file:
        file.write(nutrition100)
    with open("data_backup/classification.json", 'w') as file:
        file.write(classification)
    return redirect(url_for('get_food_items'))


@app.route("/replace_data_from_backup")
def replace_data_from_backup():
    nutrition100 = []
    classification = []
    with open("data_backup/nutrition100-bkup006.json", 'r') as file:
        nutrition100 = json.loads(file.read())
    with open("data_backup/classification-bkup006.json", 'r') as file:
        classification = json.loads(file.read())

    foods = mongo.db.nutrition100
    foods.drop()
    for ndx, each_food in enumerate(nutrition100):
        del nutrition100[ndx]["_id"]
        foods.insert_one(nutrition100[ndx])

    classes = mongo.db.classification
    classes.drop()
    for ndx, each_class in enumerate(classification):
        del classification[ndx]["_id"]
        classes.insert_one(classification[ndx])
    return redirect(url_for('get_food_items'))


if __name__ == '__main__':
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT', 8080)), debug=True)
    app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True) # Is it because of the different server?
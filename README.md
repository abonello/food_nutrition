# Nutrition Value

Milestone project from **Data Centric Development**

## Data

The data is the nutrional value per 100g (or 100ml for liquids).

* Energy (kJ)
* Energy (kcal)
* Fat
* Saturated Fat
* Carbohydrates
* Sugars
* Fibre
* Protein
* Salt
* Classification
* Shop
* Notes

Others might include:
B12 and Calcium.

I want to allow for data which in Not Available (**NA**) and values which are marked as less than (**<**).

## Pages

1. I will have a home page with some description of the project and instructions for using the application.
2. I will have a page to add data [**C**]. This will be reached from a menu item.
3. I will have a page to display [**R**] the items. I will use an accordion structure. I can do one of two things:
    1. There will be a button to lead to a more details. Here there will be a button to delete the item.
    2. All the details will show once an accordion fold is open. There will be a button to delete the item on the accordion item header.
4. In any case the delete [**D**] button will either open a modal or take the user to another page for confirmation.
5. I will have an edit page [**U**]. It will be structured like the add page but will be prepopulated with the data for the particular item to be edited. There will be a button to save the changes or leave without saving changes.
6. There will be a **Dashboard** with DC.js graphs with filters and the possibility to select an item and go to the item's detail page. (Or the accordion fold of that particular item.)

-----------

## Deploy to Heroku

Name of app: **food-nutrition**  
URI: [https://food-nutrition.herokuapp.com/](https://food-nutrition.herokuapp.com/)

I am using ***gunicorn*** server. I found that I will have to set less settings myself.  
The differences include:
1. I do NOT need to run ```heroku ps:scale web=1```
2. I do NOT need to manually set the IP and PORT variables in *settings > Reveal Config Vars*.
3. I do NOT need to *Restart all Dynos* from *More*.

In all, using gunicorn makes deploying to Heroku much easier.

The commands needed are: (using this app as example)
1. Install gunicorn
~~~~
pip3 install gunicorn
~~~~

2. Create Procfile
~~~~
echo web: gunicorn run:app > Procfile
~~~~

3. Create/Update requirements.txt
~~~~
sudo pip3 freeze --local > requirements.txt
~~~~

4. Create the Heroku on the website (allows me to set Region to EU)

5. Log in to heroku (locally, need email and password) and check the apps
~~~~
heroku login
heroku apps
~~~~

6. Initialise git, if not already done and set a remote for heroku
~~~~
git init
heroku git:remote -a food-nutrition
~~~~

7. Push to Heroku
~~~~
git push heroku master
~~~~

DONE. -- Open the app at [https://food-nutrition.herokuapp.com/]()


### Addition

To access the files on Heroku, 
1. go to **More > Run console**.
2. run the command 
~~~~
heroku run bash
~~~~
3. Use normal bash commands.

.

------------

## Database

Create a MongoDB database on mLab.  
Database name: **food**  
MONGODB VERSION: **3.6.6 (MMAPv1)**

* add user
* add collection: **nutrition100**
* created 3 documents with some data.


I had to do some changes in the code I used in previous projects.  
MONGO_DBNAME and MONGO_URI had to be used as app.config:
~~~~
app.config["MONGO_DBNAME"] = getDbName()
app.config["MONGO_URI"] = getURI()
~~~~
The port argument complained about the int() method, so now it is:
~~~~
app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True)
~~~~

### Add Food Item

Implemented **add food item**.

Now updating Heroku.  
The following code:
~~~~
from connection import getDbName, getURI
.
.
.
.
app.config["MONGO_DBNAME"] = getDbName()
app.config["MONGO_URI"] = getURI()
~~~~

does not work in Heroku.

Instead, in Heroku set environment variables for **MONGO_DBNAME** and **MONGO_URI** with the correct information.

## Classification

I created another collection in the database that will hold the different classifications of food. This will help to give unity to the data.  

I implemented the code to populate the classification input field with classes to select from in the add food item page.

I implemented adding new classes. I also added the functionality of returning to the calling page if the process is cancelled.

Implemented editing a class.


## Backups

I implemented two routes that are used either to get a backup of the database, or replace the database from a backup file. This will help me in two cases. 
1. I mess up the data during testing where it is quicker to replace the lot rather than edit indivual entries
2. The data has been messed up by someone (possibly intentionally) - I am not currently implementing a log in system.

## Dashboard

Drafted a dsahboard with 2 scatter plots - fats vs sat, carbs vs sugar.

I plan to have 4 scatter plots and a bubble chart:
1. All Fat vs Saturated
2. All Carbohydrates vs Sugar
3. Energy vs Protein (have not decided which Energy value I will use)
4. Sugar vs Salt
5. All Fat vs Carbohydrates with the following additions:
    * size of bubble - Protein
    * color - changes with quantity of Sat fat
    * border color - changes with sugar content.

I want to be able to cancel each individual filter and all filters.
I would like to be able to transfer the filters to the get_food_items view, if it is possible, to display only the selected foods in the accordion.

There is something that need to be changed in the database. Currently, the values are stored in the database with the units attached. This is not what crossfilter etc wants. Numbers should be numbers. I can do the processing in javascript(jQuery) to remove the units before passing the data to crossfilter or I can store the numbers without the units. This is the way I am choosing to do. As a result, the display of data in the accordion view will show without units unless I change the code to add them for display. This is the next step. I also have to remove the code which was adding the units when adding a new food item.


## Resetting filters for Row Chart

I had a problem with resetting the classification row chart stopping working. I tried to see how I can force an svg group name to use with redrawAll(). This led to nowhere. After a long time of trying various things such as trying to use renderlet and on renderlet (both fail), I commented out some of the code that I had and suddenly the reset link worked.  
At this point I started uncommenting one line at a time and managed to narrow the error to 
~~~~javascript
 .xAxis().ticks(4) // DO NOT ADD: This will break the reset filters 
~~~~

Adding this line will stop the resetting of the filters.

By the way the above line of code will also stop
~~~~javascript
.controlsUseVisibility(true)
~~~~
from working. Otherwise it works fine.

Now I turned the reset link to a button to match that for the scatter plots.

## Testing
I already dealt with NA values in accordion not to show units. Now the same issue appears in the modal. I also realised that if a value had to be missing completely, the units will show on their own both in the accordion and the modal.

For the purpose of testing that these two issues are dealt with, I created two test food items, one having NA in all values that will take a unit and the other has all values empty. At the moment NA will not get a unit in the accordion but will do so in the modal (needs fixing). The food item with empty values will get units in both accordion and modal (both need fixing).

The code for the accordion is in the index.html (will be renamed later on) and that for the modal is in the dashboard3.html (This is the dashboard that I will use but will be renamed.)

I added two new test items, one for when I have a value for Energy 1 but not for energy 2, and the other one for vice versa. I want to hide the **/** in such cases ( as well as when both are missing).
Combinations tested: NA "", value "", NA value, NA NA, "" NA, "" value, "" "", value value, value "", value NA

Accordion Done.


## Confirm Delete

Implemented route to delete food item. Tested by creating a test items and deleting them.  
Implemented route to delete food class. Tested by creating a test items and deleting them.

Functionality includes the ability to cancel the delete process.

## Improving classification collection.

I want the classification collection to keep track of the number of food items that use a particular classification.

Also If I come to delete a class, it the confirmation page will tell me how many food items are currently using that class. If there are any food items that use a class, I will not be able to delete that class.

1. Start by taking a current backup of the data.
2. Then, manually add a count key to all documents in the classification collection.
3. Take new backup
4. When I look at the classes route, I see a count of how many Food Items make use of that class.
5. When I create a class, it will start with a default value of count = 0.
6. When I add a food Item, the count is increased by 1.
7. When I delete a food Item, the count is decreased by 1.
8. If I change the class of a food item, its old class will be reduced by 1 and the new class is increased by 1.
9. Deleting a food class is only allowed if that class is not used by any food item.


8. What will happen when I edit a class.
    1. I need to track all the food items that used the new class and have their class edited too.
    2. Having a count of the food items using that class should make sure that all items are edited.


    Breakdown:  
    1. Click edit button
    2. Go to edit page taking id  /edit_class/<class_id>
    3. Type the edit and press Edit Class button
    4. This will take you to the update class page, still carrying id, but now have the form data /update_class/<class_id>
    5. In the update route:
        1. classification = mongo.db.classification
        2. data = request.form.to_dict()
        3. del data["action"]
        4. Get old name of classification
        5. Check that it does not match the new Name (There was a change)
        6. If there was a change [ and count > 0] ie there are food items using this class:
            1. get food table
            2. Find all food items that make use of old class name - make a list of objects
            3. ~~Extra check if needed - decide later:~~
                * ~~Get class count and check that it matches the length of list of all food items using this class~~
            4. For each food item in list of food items:
                * Change the name of the class
        7. classification.update({"_id": ObjectId(class_id)}, data)
        8. return redirect(url_for('get_classification'))
    
    
    
    ## Bug - When I edit a class the count disappears

    Fixed
    


Screen shots 

Edited with GIMP

Gif - first captured as .mov file using quickTime. Then turned into a gif using "Drop to Gif" App. 
This was further processed to reduce its size online at ezgif.com


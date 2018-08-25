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




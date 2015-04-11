#http://localhost:5000/restaurants/
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)



@app.route('/')
@app.route('/restaurants/')
def restaurantMenu():
    return render_template('restaurants.html')


@app.route('/restaurants/new')
def newRestaurant():
    return render_template('new_restaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return render_template('edit_restaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return render_template('delete_restaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return render_template('restaurant_menu.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return render_template('restaurant_menu_new.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return render_template('restaurant_menu_edit.html', restaurant_id=restaurant_id, menu_id=menu_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('restaurant_menu_delete.html', restaurant_id=restaurant_id, menu_id=menu_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
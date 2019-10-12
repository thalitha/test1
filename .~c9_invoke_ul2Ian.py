from flask import Flask, request, jsonify
from flask import Blueprint, render_template
from extensions import mongo
from bson.objectid import ObjectId

from base64 import b64encode
import os

file64 = None

app = Flask(__name__)

main = Blueprint('main', __name__)


@main.route('/')
def index():
    categories = mongo.db.categories.find({})
    bigTrends = list(mongo.db.recipes.find({}))
    for recipe in bigTrends:
        if recipe['image'] is None:
            recipe['image'] = ""
            
    return render_template('index.html', bigTrends=bigTrends, categories=categories)


@main.route('/search')
def search():
    search = request.args.get('search')
    recipes = mongo.db.recipes.find({'name': {'$regex': ".*"+search+".*"}})

    return render_template('recipe-list.html', recipes=recipes)

@main.route('/recipes')
def recipes():
    
    recipes = list(mongo.db.recipes.find({}))
    for recipe in recipes:
        if recipe['image'] is None:
            recipe['image'] = ""
    
    return render_template('recipe-list.html', recipes=recipes)

@main.route('/recipe/<id>')
def recipe(id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(id)})
    if recipe['image'] is None:
        recipe['image'] = ""

    return render_template('recipe-details.html', recipe=recipe)


@main.route('/recipe/new')
def recipeNew():

    return render_template('recipe-save.html')

@main.route('/recipe/edit/<id>')
def recipeEdit(id):
    recipe = mongo.db.recipes.find_one({'_id': ObjectId(id)})

    categories = [d.encode() for d in recipe['categories']]
    
    return render_template('recipe-save.html', recipe=recipe)
    
@main.route('/recipe/save', methods=['POST'])
def recipeSave():

    recipe = {
        'name': request.form['name'],
        'time': request.form['time'],
        'ingredients': request.form['ingredients'],
        'preparation': request.form['preparation'],
        'categories': request.form.getlist('categories[]')
    }
    
    if file64 != '':
        recipe['image'] = file64
    
    id = request.form['id']
    
    if id != "":
        mongo.db.recipes.update({'_id': ObjectId(id)},  {'$set': recipe}) 
    else:
        id = mongo.db.recipes.insert(recipe)
        
    return {'success': True, 'id': str(id)}


@main.route('/getRecipes')
def getRecipes():
    recipes = mongo.db.recipes.find({})
    # recipe_collection.insert({'name': 'cake'})

    return recipes[0]['name']

# Categories
@main.route('/categories/GetAll')
def categoriesGetAll():
    categories = mongo.db.categories.find({}).sort('name', 1)
    
    output = []
    for category in categories:
        output.append(
            {'id': str(category['_id']), 'text': category['name']})

    return jsonify(output)


@main.route('/file-upload', methods=['POST'])
def fileUpload():
    global file64

    f = request.files.get('file')
    f.save(os.path.join('static/images', f.filename))

    file64 = f.filename
    # if request.method == 'POST':
    #     image = request.files.get('file')
    #     file64 = b64encode(image.read())
    #f.save(os.path.join('the/path/to/save', f.filename))

    return file64

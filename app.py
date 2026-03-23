from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

client = MongoClient('mongodb+srv://manthansomani860:Manthan.somani86@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority')
db = client['inventory_db']
collection = db['items']

@app.route('/')
def index():
    search_query = request.args.get('search')
    
    if search_query:
        query = {"$or": [
            {"name": {"$regex": search_query, "$options": "i"}},
            {"imeis": {"$regex": search_query, "$options": "i"}}
        ]}
        items = list(collection.find(query))
    else:
        items = list(collection.find())
        
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    quantity = request.form.get('quantity')
    imeis = request.form.get('imeis')
    photo = request.files.get('photo')
    
    filename = ""
    if photo and photo.filename != "":
        filename = photo.filename
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    collection.insert_one({
        'name': name, 
        'price': price, 
        'description': description,
        'quantity': quantity, 
        'imeis': imeis, 
        'photo': filename
    })
        
    return redirect('/')

@app.route('/update/<id>', methods=['POST'])
def update(id):
    new_qty = request.form.get('quantity')
    new_price = request.form.get('price')
    
    collection.update_one(
        {'_id': ObjectId(id)}, 
        {'$set': {
            'quantity': new_qty, 
            'price': new_price
        }}
    )
    return redirect('/')
@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
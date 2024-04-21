from django.shortcuts import render, get_object_or_404
from pymongo import MongoClient
from bson import ObjectId
from django.contrib.auth.decorators import login_required

from item.models import Item

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['campus_market']  # Replace 'campus_market' with your MongoDB database name
items_collection = db['items']  # Collection for storing item data

@login_required
def index(request):
    # Retrieve items belonging to the current user from MongoDB
    user_items = items_collection.find({'created_by': str(request.user.id)})

    return render(request, 'dashboard/index.html', {
        'items': user_items,
    })

def home(request):
    # Retrieve all items from MongoDB
    items = items_collection.find()

    return render(request, 'home.html', {'items': items})

def item_list(request):
    # Retrieve all items from MongoDB
    items = items_collection.find()

    return render(request, 'item_list.html', {'items': items})

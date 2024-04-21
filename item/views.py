from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from pymongo import MongoClient
from bson import ObjectId


from .forms import NewItemForm, EditItemForm
from .models import Category, Item

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['campus_market']  # Replace 'campus_market' with your MongoDB database name
items_collection = db['items']  # Collection for storing item data

def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()

    # MongoDB query to filter items
    filter_query = {'is_sold': False}
    if category_id:
        filter_query['category_id'] = int(category_id)
    if query:
        # Perform case-insensitive search on name and description
        filter_query['$or'] = [
            {'name': {'$regex': query, '$options': 'i'}},
            {'description': {'$regex': query, '$options': 'i'}}
        ]

    items = items_collection.find(filter_query)

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    item = items_collection.find_one({'_id': ObjectId(pk)})
    related_items = items_collection.find({
        'category_id': item['category_id'],
        'is_sold': False,
        '_id': {'$ne': ObjectId(pk)}
    }).limit(3)

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item_data = form.cleaned_data
            item_data['created_by'] = request.user.id

            # Insert new item document into MongoDB
            item_id = items_collection.insert_one(item_data).inserted_id

            return redirect('item:detail', pk=str(item_id))
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = items_collection.find_one({'_id': ObjectId(pk), 'created_by': request.user.id})

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES)

        if form.is_valid():
            updated_data = form.cleaned_data

            # Update existing item document in MongoDB
            items_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_data})

            return redirect('item:detail', pk=pk)
    else:
        form = EditItemForm(initial=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    # Delete item document from MongoDB
    items_collection.delete_one({'_id': ObjectId(pk), 'created_by': request.user.id})

    return redirect('dashboard:index')

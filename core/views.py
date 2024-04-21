from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from pymongo import MongoClient
from item.models import Category, Item


from .forms import SignupForm

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['campus_market']  # Replace 'campus_market' with your MongoDB database name
users_collection = db['users']  # Collection for storing user data

def index(request):
    # Your existing code to retrieve items and categories
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            # Save user data to MongoDB
            user_data = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                # Add more fields as needed
            }
            users_collection.insert_one(user_data)

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })

@login_required
def logout_user(request):
    logout(request)
    return redirect('dashboard:index')

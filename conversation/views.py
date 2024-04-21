from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from item.models import Item
from .forms import ConversationMessageForm
import pymongo
from pymongo import MongoClient
from bson import ObjectId

# Handling database connection
def get_database_connection():
    client = MongoClient('mongodb://localhost:27017/')
    return client['campus_market']

@login_required
def new_conversation(request, item_pk):
    db = get_database_connection()
    conversation_collection = db['conversation']
    
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('dashboard:index')
    
    conversation_query = {
        'item_id': str(item_pk),
        'members': {'$in': [str(request.user.id)]}
    }
    existing_conversation = conversation_collection.find_one(conversation_query)

    if existing_conversation:
        return redirect('conversation:detail', pk=existing_conversation['_id'])

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            new_conversation = {
                'item_id': str(item_pk),
                'members': [str(request.user.id), str(item.created_by.id)]
            }
            conversation_id = conversation_collection.insert_one(new_conversation).inserted_id

            conversation_message = form.cleaned_data['content']
            conversation_collection.update_one(
                {'_id': ObjectId(conversation_id)},
                {'$push': {'messages': {'content': conversation_message, 'created_by': str(request.user.id)}}}
            )

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form
    })

@login_required
def inbox(request):
    db = get_database_connection()
    conversation_collection = db['conversation']

    conversations = conversation_collection.find({'members': {'$in': [str(request.user.id)]}})

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    db = get_database_connection()
    conversation_collection = db['conversation']

    conversation = conversation_collection.find_one({'_id': ObjectId(pk), 'members': {'$in': [str(request.user.id)]}})

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.cleaned_data['content']
            conversation_collection.update_one(
                {'_id': ObjectId(pk)},
                {'$push': {'messages': {'content': conversation_message, 'created_by': str(request.user.id)}}}
            )

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })

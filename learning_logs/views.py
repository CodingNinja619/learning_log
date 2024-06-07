from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """The topics page"""
    topics = Topic.objects.order_by("date_added")
    context = {"topics": topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """The individual topic page"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.all()
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)

def new_topic(request):
    """Add a new topic"""
    if request.method != "POST":
        # No data sumibtted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    # Try not to fill in the form later to see error messages
    context = {'form': form}
    return render(request, "learning_logs/new_topic.html", context)

def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False) # IT CREATES AN OBJECT OF THE SPECIFIED MODEL
            new_entry.topic = topic
            new_entry.save()
            # Do I refer to a url or to a view???
            # To a view. it IS SAID in the book
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display blank or invalid form
    context = {"topic": topic, "form": form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != "POST":
        form = EntryForm(instance=entry)
        # form = EntryForm()
    else:
        form = EntryForm(instance=entry, data=request.POST)
        # form = EntryForm(data=request.POST)
        # HOW DOES DJANGO KNOW WHAT ENTRY TO EDIT?
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)
      

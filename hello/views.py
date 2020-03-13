from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Greeting
from .forms import Form1

# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Form1(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/calculatesimilarity/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Form1()

    return render(request, 'index.html', {'form': form})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

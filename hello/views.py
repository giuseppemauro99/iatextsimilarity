from xml.dom.minidom import Document

import spacy
import os
import pymongo as pymongo
from bson import ObjectId
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Greeting
from .forms import Form1

myclient = pymongo.MongoClient(os.environ.get('MONGODB_URI'))
mydb = myclient.get_default_database()


# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Form1(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            request.session['file1'] = request.FILES['file1']
            request.session['file2_query'] = request.FILES['file2_query']
            uploadToMongoDB(request.FILES['file1'], request.FILES['file2_query'], request)
            # redirect to a new URL:
            return HttpResponseRedirect('/calculatesimilarity/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Form1()

    return render(request, 'index.html', {'form': form})


def uploadToMongoDB(file1, file2, request):
    text_file1 = ""
    text_file2 = ""
    for line in file1:
        text_file1 = text_file1 + str(line.decode("UTF-8"))
    for line in file2:
        text_file2 = text_file2 + str(line.decode("UTF-8"))

    text1_json = {'data': text_file1}
    text2_json = {'data': text_file2}

    f1 = mydb["files"].insert_one(text1_json)
    f2 = mydb["files"].insert_one(text2_json)

    request.session['file1'] = str(f1.inserted_id)
    request.session['file2_query'] = str(f2.inserted_id)

    return True


def calculatesimilarity(request):
    file1id = request.session['file1']
    file2id = request.session['file2_query']

    file1 = mydb.get_collection("files").find_one_and_delete({'_id': ObjectId(file1id)})["data"]
    file2 = mydb.get_collection("files").find_one_and_delete({'_id': ObjectId(file2id)})["data"]

    return render(request, 'calculatesimilarity.html', {'id_file1': file1id, 'id_file2': file2id,
                                                        'sim_matrix': similarityMatrix(file1, file2)})


def similarityMatrix(file1, file2):
    nlp = spacy.load("it_core_news_sm")
    # bisogna risolvere il problema con la grandezza della matrice
    col = len(file1.splitlines())
    row = len(file2.splitlines())+1

    sim_matrix = [[0 for i in range(row)] for j in range(col)]
    i = j = 0
    for line1 in file1.splitlines():
        for line2 in file2.splitlines():
            doc1 = nlp(line1)
            doc2 = nlp(line2)
            sim_matrix[i][j] = doc1.similarity(doc2)
            j = j + 1
        i = i + 1

    return sim_matrix


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

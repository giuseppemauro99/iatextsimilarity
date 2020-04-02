import csv
import datetime
from datetime import datetime
from wsgiref.util import FileWrapper

import spacy
import os, io
import pymongo as pymongo
from bson import ObjectId
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404

from .models import Greeting
from .forms import Form1

#MONGO_DB_URI = "mongodb://heroku_166t21vc:chbme62a0ama4gda9p203bgs0e@ds113935.mlab.com:13935/heroku_166t21vc?retryWrites=false"
MONGO_DB_URI = "mongodb://"+os.environ.get("MONGODB_USERNAME")+":"+os.environ.get("MONGODB_PASSWORD")+"@"+"mongodb"+":27017"

myclient = pymongo.MongoClient(MONGO_DB_URI)
#mydb = myclient["heroku_166t21vc"]
mydb = myclient["django_db"]


# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Form1(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process file to DB
            request.session['file1'] = request.FILES['file1']
            request.session['file2_query'] = request.FILES['file2_query']
            uploadToMongoDB(request.FILES['file1'], request.FILES['file2_query'], request)
            # process label
            request.session["label1"] = form.cleaned_data["label1"]
            request.session["label1_start"] = str(form.cleaned_data["label1_interval"]).split("-")[0]
            request.session["label1_finish"] = str(form.cleaned_data["label1_interval"]).split("-")[1]

            request.session["label2"] = form.cleaned_data["label2"]
            request.session["label2_start"] = str(form.cleaned_data["label2_interval"]).split("-")[0]
            request.session["label2_finish"] = str(form.cleaned_data["label2_interval"]).split("-")[1]

            request.session["label3"] = form.cleaned_data["label3"]
            request.session["label3_start"] = str(form.cleaned_data["label3_interval"]).split("-")[0]
            request.session["label3_finish"] = str(form.cleaned_data["label3_interval"]).split("-")[1]

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

    start = datetime.now()
    sim_matrix, colth, rowth = similarityMatrix(file1, file2, request)
    finish = datetime.now()

    return render(request, 'calculatesimilarity.html',
                  {'tempo_di_esecuzione': (finish - start), 'sim_matrix': sim_matrix})


def similarityMatrix(file1, file2, request):
    nlp = spacy.load("it_core_news_sm")

    buf1 = io.StringIO(file1)
    lines1 = buf1.readlines()
    row = len(lines1)

    buf2 = io.StringIO(file2)
    lines2 = buf2.readlines()
    col = len(lines2)

    sim_matrix = [["string" for x in range(col)] for y in range(row)]
    i = j = 0

    for line1 in lines1:
        j = 0
        for line2 in lines2:
            doc1 = nlp(line1)
            doc2 = nlp(line2)
            val = f"{(doc1.similarity(doc2) * 100) :.2f}"  # calcolo la similarità, la trasformo in percentuale e prendo solo 2 cifre decimali
            sim_matrix[i][j] = val2Label(val, request)
            j = j + 1
        i = i + 1

    return sim_matrix, lines1, lines2


def val2Label(val, request):
    if float(request.session["label1_start"]) <= float(val) < float(request.session["label1_finish"]):
        return request.session["label1"]
    if float(request.session["label2_start"]) <= float(val) < float(request.session["label2_finish"]):
        return request.session["label2"]
    if float(request.session["label3_start"]) <= float(val) < float(request.session["label3_finish"]):
        return request.session["label3"]

    return val


def db(request):
    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

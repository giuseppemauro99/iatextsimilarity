from xml.dom.minidom import Document

import gensim
import numpy as np
import pymongo as pymongo
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from nltk import sent_tokenize, word_tokenize

from .models import Greeting
from .forms import Form1

# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Form1(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            # process the data in form.cleaned_data as required
            request.session['file1'] = request.FILES['file1']
            request.session['file2_query'] = request.FILES['file2_query']
            uploadToMongoDB(request.FILES['file1'],request.FILES['file2_query'],request)
            # redirect to a new URL:
            return HttpResponseRedirect('/calculatesimilarity/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Form1()

    return render(request, 'index.html', {'form': form})

def uploadToMongoDB(file1,file2,request):
    myclient = pymongo.MongoClient("mongodb://admin:Admin99@ds113935.mlab.com:13935/heroku_166t21vc")
    mydb = myclient["heroku_166t21vc"]

    text_file1 = ""
    text_file2 = ""
    for line in file1:
        text_file1 = text_file1 + line
    for line in file2:
        text_file2 = text_file2 + line

    f1 = mydb["files"].insert_one(text_file1)
    f2 = mydb["files"].insert_one(text_file2)

    request.session['file1'] = f1.inserted_id
    request.session['file2_query'] = f2.inserted_id

    return True

def calculatesimilarity(request):
    file1id = request.session['file1']
    file2id = request.session['file2_query']

    return render(request, 'calculatesimilarity.html', {'id_file1': file1id, 'id_file2': file2id})


def similarity(request, id):
    document = get_object_or_404(Document, id=id)
    file_docs = []
    file2_docs = []
    avg_sims = []
    with open('media/' + document.document.name) as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file_docs.append(line)

    length_doc1 = len(file_docs)

    gen_docs = [[w.lower() for w in word_tokenize(text)]
                for text in file_docs]

    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('workdir/', tf_idf[corpus],
                                          num_features=len(dictionary))

    with open('media/' + document.document2.name) as f:
        tokens = sent_tokenize(f.read())
        for line in tokens:
            file2_docs.append(line)

    for line in file2_docs:
        query_doc = [w.lower() for w in word_tokenize(line)]
        query_doc_bow = dictionary.doc2bow(query_doc)
        query_doc_tf_idf = tf_idf[query_doc_bow]
        print('Comparing Result:', sims[query_doc_tf_idf])
        sum_of_sims = (np.sum(sims[query_doc_tf_idf], dtype=np.float32))
        avg = sum_of_sims / len(file_docs)
        print(f'avg: {sum_of_sims / len(file_docs)}')
        avg_sims.append(avg)
    total_avg = np.sum(avg_sims, dtype=np.float)
    print(total_avg)
    percentage_of_similarity = round(float(total_avg) * 100)
    if percentage_of_similarity >= 100:
        percentage_of_similarity = 100

    return render(request, 'document.html', {
        'percentage_of_similarity': percentage_of_similarity,
    })


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

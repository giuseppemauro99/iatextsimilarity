from django import forms
from django.forms import models


class  Form1 ( forms.Form ):
     file1 = models.FileField(label="Inserisci file 1")
     file2_query = models.FileField(label = "Inserisci file 2")
from django import forms


class  Form1 ( forms.Form ):
     file1 = forms.FileField(label="Inserisci file 1",upload_to='uploads/')
     file2_query = forms.FileField(label="Inserisci file 2",upload_to='uploads/')
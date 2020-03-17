from django import forms


class  Form1 ( forms.Form ):
     file1 = forms.FileField(label="Inserisci file 1")
     file2_query = forms.FileField(label="Inserisci file 2")
     label1 = forms.CharField(label="Nome etichetta")
     label1_interval = forms.CharField(label='Intervallo',
                         widget=forms.TextInput(attrs={'placeholder': 'Intervallo etichetta, es. 0.0-20.5'}))
     label2 = forms.CharField(label="Nome etichetta")
     label2_interval = forms.CharField(label='Intervallo',
                                       widget=forms.TextInput(
                                            attrs={'placeholder': 'Intervallo etichetta, es. 20.5-50.0'}))
     label3 = forms.CharField(label="Nome etichetta")
     label3_interval = forms.CharField(label='Intervallo',
                                       widget=forms.TextInput(
                                            attrs={'placeholder': 'Intervallo etichetta, es. 50.0-100.0'}))
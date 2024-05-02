from django import forms
from .models import Pays

class ListeIngredientsImport(forms.Form):
    file = forms.FileField()

    # pays = forms.ModelChoiceField(queryset=Pays.objects.all())

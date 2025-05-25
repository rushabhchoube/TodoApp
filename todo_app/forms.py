from .models import Tasks
from django import forms

class TodoForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name','priority','date']
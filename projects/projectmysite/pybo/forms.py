from django import forms
from pybo.models import Question
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questionfields = ['subject','content']
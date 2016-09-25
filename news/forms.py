from django import forms

class CommentForm(forms.Form):
    text = forms.CharField(label='Comment', max_length=200)

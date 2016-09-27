from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Article

class CommentForm(forms.Form):
	text = forms.CharField(label='Comment', max_length=200)

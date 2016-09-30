from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Article

COMMENT_STATUSES = (
	('NEW', 'New'),
	('APP', 'Approved'),
	('REJ', 'Rejected'),
)

class CommentForm(forms.Form):
	text = forms.CharField(label='Comment', max_length=200)

class CommentReviewForm(forms.Form):
	status = forms.ChoiceField(choices=COMMENT_STATUSES)
	reviewer_comment = forms.CharField(max_length=200, required=False)



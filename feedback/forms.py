from django import forms

COMMENT_STATUSES = (
    ('NEW', 'New'),
    ('APP', 'Approved'),
    ('REJ', 'Rejected'),
)

class CommentForm(forms.Form):
    text = forms.CharField(
        label='Comment',
        max_length=200,
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'placeholder': 'Write a comment...'})
    )


class CommentReviewForm(forms.Form):
    status = forms.ChoiceField(choices=COMMENT_STATUSES)
    reviewer_comment = forms.CharField(max_length=200, required=False)
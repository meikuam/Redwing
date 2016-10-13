from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}
        )
    )
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
    )


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        ),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm password'}
        ),
    )

from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Listing, Category, Bid, Comment


class AddListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(
    ), empty_label="Select a Category", widget=forms.Select(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'image': forms.URLInput(attrs={'class': 'form-control mb-3'}),
            # 'category': forms.Select(attrs={'class': 'form-control mb-3'}, choices=Category.CATEGORY_CHOICES),
        }


class BidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = False

    class Meta:
        model = Bid
        fields = '__all__'
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter your bid amount'
            }),
            'listing': forms.HiddenInput(),
            'bidder': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = False

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Write a comment'
            })
        }

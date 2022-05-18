# Review Add Form
from .models import ProductReview
from django import forms
class ReviewAddForm(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')
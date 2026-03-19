from django import forms
from .models import Place

class NewPlaceForm(forms.ModelForm):
    class Meta:
        # more than one form can reference the same model.
        model = Place
        fields = ('name', 'visited')

class DateInput(forms.DateInput):
    input_type='date'

class TripReviewForm(forms.ModelForm):
    # form is created using the model data from the place model.
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo')
        # widgets can be used to customize the format and how data input is handled in a form
        widgets = {
            'date_visited': DateInput()
        }
        
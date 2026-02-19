from django import forms

class EnrollmentForm(forms.Form):
    # For a simple POST-only enroll action we don't need fields, but keep this for extensibility
    confirm = forms.BooleanField(required=False, initial=True, widget=forms.HiddenInput)
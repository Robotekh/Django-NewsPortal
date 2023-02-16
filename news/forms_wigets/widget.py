from django import forms


class MyDateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'
"""Here are forms used in comparator app"""


from django import forms

class SearchForm(forms.Form):
    """Form which permit to user to search for a food item"""
    search_widget = forms.TextInput(attrs={'placeholder': 'Aliment...', 'class': 'input-xl'})
    user_input = forms.CharField(label='', max_length=50, widget=search_widget)

from django import forms


class CompostOfferForm(forms.Form):
    animal_mature_quantities = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control quantities', 'id': 'animal-mature-quantities', 'name': 'manure'}))
    plant_based_fertilizers_quantities = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control quantities', 'id': 'plant-based-fertilizers-quantities', 'name': 'plant_fertilizers'}))
    biodegradable_fertilizers_quantities = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control quantities', 'id': 'biodegradable-fertilizers-qauntities', 'name': 'biodegradable_fertilizers'}))
    date_range = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'my-date-picker', 'name': 'date_range', 'placeholder': 'Select Date Range'}))
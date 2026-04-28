from django import forms
from .models import Booking, Customer

class BookingForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

class AvailabilityForm(forms.Form):
    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
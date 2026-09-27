from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone', 'city', 'pincode', 'address')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'resize-none'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from django.contrib.auth.models import User
from .models import Traveler, ContactMessage, UserProfile, Destination

class TravelerForm(forms.ModelForm):
    class Meta:
        model = Traveler
        fields = ['name', 'email', 'phone', 'destination']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 98765 43210'}),
            'destination': forms.TextInput(attrs={'placeholder': 'Enter destination city'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 98765 43210'}),
            'subject': forms.TextInput(attrs={'placeholder': "What's your inquiry about?"}),
            'message': forms.Textarea(attrs={'placeholder': 'Tell us about your travel plans or questions...', 'rows': 5}),
        }

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username',
            'class': 'form-input'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'class': 'form-input'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '+91 98765 43210',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a strong password',
            'class': 'form-input'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-input'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': '+91 98765 43210'}),
            'address': forms.Textarea(attrs={'placeholder': 'Your full address', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            profile.save()
        return profile

# NEW: Destination Form (Admin Only)
class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'country', 'description', 'category', 'image_url', 
                  'price_per_day', 'duration_days', 'highlights', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Eiffel Tower'}),
            'country': forms.TextInput(attrs={'placeholder': 'e.g., France'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe this beautiful destination...', 'rows': 4}),
            'image_url': forms.URLInput(attrs={'placeholder': 'https://images.unsplash.com/...'}),
            'price_per_day': forms.NumberInput(attrs={'placeholder': '5000'}),
            'duration_days': forms.NumberInput(attrs={'placeholder': '7'}),
            'highlights': forms.Textarea(attrs={'placeholder': 'Eiffel Tower, Louvre Museum, Seine River Cruise', 'rows': 3}),
        }
from django import forms
from .models import HospitalConfiguration

class HospitalConfigurationForm(forms.ModelForm):
    class Meta:
        model = HospitalConfiguration
        fields = [
            'hospital_name', 
            'hospital_subtitle', 
            'hospital_address', 
            'hospital_phone', 
            'hospital_email', 
            'hospital_footer_text'
        ]
        widgets = {
            'hospital_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none',
                'placeholder': 'Enter hospital name'
            }),
            'hospital_subtitle': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none',
                'placeholder': 'Sub-text (e.g. Pharmacy & Wellness Center)'
            }),
            'hospital_address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none h-24',
                'placeholder': 'Full address'
            }),
            'hospital_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none',
                'placeholder': 'Contact phone'
            }),
            'hospital_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none',
                'placeholder': 'Contact email'
            }),
            'hospital_footer_text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all outline-none h-20',
                'placeholder': 'Footer text on bill'
            }),
        }

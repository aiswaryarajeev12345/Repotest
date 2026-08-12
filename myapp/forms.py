from django import forms

from .models import Alert, HelpRequest




class AlertForm(forms.ModelForm):

    class Meta:

        model = Alert

        fields = [
            'disaster_type',
            'area',
            'alert_message'
        ]

        widgets = {

            'disaster_type': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter disaster type'
                }
            ),

            'area': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter affected area'
                }
            ),

            'alert_message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter emergency alert message'
                }
            ),

        }




class HelpRequestUpdateForm(forms.ModelForm):

    class Meta:

        model = HelpRequest

        fields = [
            'status',
            'response_result'
        ]

        widgets = {

            'status': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'response_result': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter the help provided or result'
                }
            ),

        }
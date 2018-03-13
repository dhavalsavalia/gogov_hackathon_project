from django import forms
from .models import MainProject


class MainProjectForm(forms.ModelForm):
    class Meta:
        model = MainProject
        fields = [
            'PROJECT_NAME',
            'HOMEPAGE',
        ]

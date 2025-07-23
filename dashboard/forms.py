from  django import forms

class DashboardForm(forms.Form):
    text=forms.CharField(max_length=100,label="Enter your search ")
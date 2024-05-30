from .models import Subscription
from django import forms
from .models import ConfigurationSetting
from tinymce.widgets import TinyMCE


class ConfigurationSettingForm(forms.ModelForm):
    class Meta:
        model = ConfigurationSetting
        fields = '__all__'
        widgets = {
            'text_value': TinyMCE(attrs={'rows': 20}),
        }


class SubscriptionForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Subscription
        fields = ['email', 'first_name', 'last_name']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            instance.save()
        return instance

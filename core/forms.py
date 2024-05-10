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

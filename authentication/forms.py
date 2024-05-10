from typing import Any
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Account


class AccountsAdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = (
            'email', 'first_name', 'other_names', 'last_name', 'phone_number', 'user_permissions'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_fields['phone_number'].required = True


class AccountsAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Account

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.base_fields.get('phone_number', None):
            self.base_fields['phone_number'].required = True

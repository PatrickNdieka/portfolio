from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from .models import Account, Profile, Role
from .forms import AccountsAdminCreationForm, AccountsAdminChangeForm


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile
    fields = ('avatar', 'profile_picture',)
    readonly_fields = ('avatar',)


class AccountsAdmin(UserAdmin):
    add_form = AccountsAdminCreationForm
    form = AccountsAdminChangeForm
    model = Account
    list_display = ['email', 'first_name',
                    'last_name', 'phone_number', 'is_admin']
    fieldsets = (
        ('Personal info', {
         'fields': ('email', 'first_name', 'last_name', 'phone_number')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name',
                'phone_number', 'password1', 'password2',
            ),
        }),
    )

    readonly_fields = ('email', 'date_joined', 'last_login')

    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('email', 'first_name', 'last_name', 'is_admin')
    inlines = (ProfileInlineAdmin,)

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        if obj and request.user.is_superuser:
            fieldsets.append(
                ('Permissions', {'fields': ('is_admin', 'is_active', 'groups')}))
        return tuple(fieldsets)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = [*super().get_readonly_fields(request, obj)]
        if obj and obj.is_superuser:
            readonly_fields.extend(
                ['is_admin', 'is_active', 'groups'])
        elif obj and obj != request.user:
            readonly_fields.extend(['first_name', 'last_name', 'phone_number'])
        return tuple(readonly_fields)

    def get_inline_instances(self, request, obj=None):
        if obj and obj == request.user:
            return super().get_inline_instances(request, obj)
        return []

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request).select_related('profile')
        return super().get_queryset(request).filter(
            pk=request.user.pk).select_related('profile')

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return super().has_add_permission(request)
        else:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return super().has_change_permission(request, obj)
        elif request.user == obj:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_superuser:
            return False
        elif request.user.is_superuser:
            return super().has_delete_permission(request, obj)
        else:
            return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.has_default_password = True
            obj.is_admin = True
        return super().save_model(request, obj, form, change)


class RoleAdmin(GroupAdmin):
    pass


admin.site.unregister(Group)
admin.site.register(Account, AccountsAdmin)
admin.site.register(Role, RoleAdmin)

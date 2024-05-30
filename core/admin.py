from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .models import (
    ProjectPortfolio, ConfigurationSetting, Section, SectionInformation,
    Service, Skill, Subscription
)


class SectionInlineAdmin(admin.TabularInline):
    model = Section
    empty_value_display = "-Select option-"
    extra = 0


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent',)
    fields = ('name',)
    readonly_fields = ('parent',)
    autocomplete_fields = ('parent',)
    search_fields = ('name', 'parent__name', 'sub_sections__name')
    inlines = [SectionInlineAdmin]


class SectionInformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'section',)
    list_filter = ('value_type',)
    list_select_related = ('section',)
    autocomplete_fields = ('section',)
    search_fields = ('title', 'html_value', 'image_value', 'section__name')

    def value(self, obj):
        if obj and (obj.value_type == 'html') and len(obj.get_value) > 200:
            return obj.get_value[:75] + ' . . . ' + obj.get_value[-75:]
        else:
            return obj.get_value

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:  # Check if this is an update (change=True)
            selected_value_type = obj.value_type
            for field in obj._meta.get_fields():
                if field.name.endswith('_value') and field.concrete:
                    if field.name == f'{selected_value_type}_value':
                        continue  # Skip the selected value field
                    setattr(obj, field.name, '')

            obj.save()  # Save changes to the current object


class SkillInlineAdmin(admin.TabularInline):
    model = Skill.projects.through
    empty_value_display = "-Select option-"
    extra = 0


class ServiceInlineAdmin(admin.TabularInline):
    model = Service.projects.through
    empty_value_display = "-Select option-"
    extra = 0


class SkillAdmin(admin.ModelAdmin):
    inlines = (SkillInlineAdmin,)
    exclude = ('projects',)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured')
    list_editable = ('featured',)
    inlines = (ServiceInlineAdmin,)
    exclude = ('projects',)


class ProjectPortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'status', 'published_on', 'author',)
    list_display_links = ('title',)
    list_editable = ('status',)
    list_filter = ('status', 'author',)
    list_select_related = ('author',)
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = ('author',)
    date_hierarchy = "published_on"
    empty_value_display = "-Select option-"
    radio_fields = {"status": admin.HORIZONTAL,
                    'content_type': admin.HORIZONTAL}
    inlines = (SkillInlineAdmin, ServiceInlineAdmin)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        if obj.featured:
            # Check if there are any other featured projects
            existing_featured_projects = ProjectPortfolio.objects.filter(
                featured=True).exclude(pk=obj.pk)
            if existing_featured_projects.exists():
                existing_featured_projects.update(featured=False)
        super().save_model(request, obj, form, change)


class ConfigurationSettingAdmin(admin.ModelAdmin):
    list_display = ('configuration', 'key', 'value', 'parent')
    list_filter = ('value_type',)
    list_select_related = ('parent',)
    search_fields = (
        'key', 'email_value', 'file_value', 'html_value',
        'image_value', 'phone_value', 'text_value', 'url_value',
        'parent__key', 'children__key'
    )
    autocomplete_fields = ('parent',)

    def value(self, obj):
        if obj and (obj.value_type in ['text', 'html']) and len(obj.get_value) > 200:
            return obj.get_value[:75] + ' . . . ' + obj.get_value[-75:]
        else:
            return obj.get_value

    def configuration(self, obj):
        return obj

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if change:  # Check if this is an update (change=True)
            selected_value_type = obj.value_type

            for field in obj._meta.get_fields():
                if field.name.endswith('_value') and field.concrete:
                    if field.name == f'{selected_value_type}_value':
                        continue  # Skip the selected value field
                    setattr(obj, field.name, '')

            obj.save()  # Save changes to the current object


admin.site.register(ConfigurationSetting, ConfigurationSettingAdmin)
admin.site.register(ProjectPortfolio, ProjectPortfolioAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SectionInformation, SectionInformationAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Subscription)

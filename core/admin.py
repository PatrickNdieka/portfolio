from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import ProjectPortfolio, Skill


class SkillInlineAdmin(admin.TabularInline):
    model = Skill.projects.through
    empty_value_display = "-Select option-"
    extra = 0


class SkillAdmin(admin.ModelAdmin):
    inlines = (SkillInlineAdmin,)
    exclude = ('projects',)


class ProjectPortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'status', 'published_on', 'author')
    list_display_links = ('title',)
    list_editable = ('featured', 'status')
    list_filter = ('status', 'author')
    list_select_related = ('author',)
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ('author',)
    date_hierarchy = "published_on"
    empty_value_display = "-Select option-"
    radio_fields = {"status": admin.HORIZONTAL}
    inlines = (SkillInlineAdmin,)


admin.site.register(ProjectPortfolio, ProjectPortfolioAdmin)
admin.site.register(Skill, SkillAdmin)

from django.contrib import admin

from issue_catcher.models import Language, Label, User

admin.site.register(Language)
admin.site.register(Label)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'display_language', 'display_label',)

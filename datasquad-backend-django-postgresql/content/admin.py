from django.contrib import admin

from .models import NewsPost, TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_published", "updated_at")
    list_editable = ("order", "is_published")
    search_fields = ("name", "role", "mission")
    list_filter = ("is_published",)


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "date_label", "order", "is_published", "updated_at")
    list_editable = ("order", "is_published")
    search_fields = ("title", "body")
    list_filter = ("is_published",)

from django.contrib import admin
from django.utils.html import format_html
from .models import Topic, User, Outcome, Course


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptor')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptor')


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('code', 'descriptor')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'upcoming', 'show_course_url')
    filter_horizontal = ('outcomes',)
    ordering = ['code']

    def show_course_url(self, obj):
        return format_html("<a href='{url}'>Link</a>", url=obj.hyperlink)

    show_course_url.short_description = "Course URL"


admin.site.site_header = "Oracle Administration"
admin.site.site_title = "Oracle Site Admin"
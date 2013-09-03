# -*- coding: utf-8 -*-
# from django.db import models
from django.contrib import admin
from apps.videoblog.models import Video, ViewStats, VideoTags, Feedback, Images
from tagging_autocomplete.widgets import TagAutocomplete
# from django.forms import TextInput


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'ip', 'email', 'date')


class ViewStatsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'video_from', 'video_to', 'views')


class Images_Inline(admin.TabularInline):
    model = Images

class VideoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        VideoTags: {'widget': TagAutocomplete}
    }
    date_hierarchy = 'date'
    list_filter = ('hoster','sites')
    search_fields = ['name', 'desc']
    list_display = ('name', 'hoster', 'tags')
    inlines = [
        Images_Inline,
    ]
    # list_editable = ('name', 'tags')
    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size': '60'})},
    # }




admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(ViewStats, ViewStatsAdmin)

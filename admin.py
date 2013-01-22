# -*- coding: utf-8 -*-
# from django.db import models
from django.contrib import admin
from videoblog.models import Video, ViewStats, VideoTags
from tagging_autocomplete.widgets import TagAutocomplete


class ViewStatsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'video_from', 'video_to', 'views')


class VideoAdmin(admin.ModelAdmin):
    formfield_overrides = {
        VideoTags: {'widget': TagAutocomplete}
    }
    list_display = ('__unicode__', 'hoster', 'tags')


admin.site.register(Video, VideoAdmin)
admin.site.register(ViewStats, ViewStatsAdmin)

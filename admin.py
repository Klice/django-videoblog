# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from videoblog.models import Video, ViewStats

class ViewStatsAdmin(admin.ModelAdmin):
        list_display = ('__unicode__','video_from','video_to','views',)


admin.site.register(Video)
admin.site.register(ViewStats, ViewStatsAdmin)

# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from apps.videoblog.models import Video
from django.db.models import Q


class LatestEntriesFeed(Feed):
    title = "Peegirl.info"
    link = "/"
    description = "Новые видео и фото"

    def items(self):
        return Video.on_site.filter(~Q(name='')&~Q(hoster='text')).order_by('-date')[:20]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.desc

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.get_absolute_url()
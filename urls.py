from django.conf.urls import patterns
from django.views.generic import TemplateView
from django.conf.urls.defaults import *
from apps.videoblog.feeds import LatestEntriesFeed

urlpatterns = patterns('',
    (r'add_video_url/$', 'apps.videoblog.views.Add_Video_URL'),
    (r'add_video_url/$', 'apps.videoblog.views.Add_Video_URL', {}),
    (r'movie/(?P<name>.+)-(?P<video_id>\d+)/$', 'apps.videoblog.views.detail_video', {}, 'detail_video'),
    (r'movie/delete/(?P<id>\d+)/$',  'apps.videoblog.views.delete_video', {}, 'delete_video'),
    (r'movie/edit_desc/(?P<id>\d+)/$',  'apps.videoblog.views.edit_video_desc', {}, 'edit_video_desc'),
    (r'movie/edit_tags/(?P<id>\d+)/$',  'apps.videoblog.views.edit_video_tags', {}, 'edit_video_tags'),
    (r'archive/(?P<month>\d+)/$', 'apps.videoblog.views.videolist', {}, 'video_list_archive'),

    (r'movie/vote_good/(?P<id>\d+)/$', 'apps.videoblog.views.video_vote', {'res': 1}, 'video_vote_good'),
    (r'movie/vote_bad/(?P<id>\d+)/$', 'apps.videoblog.views.video_vote', {'res': -1}, 'video_vote_bad'),

    (r'add_amazon_url/$', 'apps.videoblog.views.Add_Video_Amazon_URL'),

    (r'tag/(?P<tag>[\w ^/\-]+)/$', 'apps.videoblog.views.videolist', {}, 'tag_list'),

    (r'tags/$', 'apps.videoblog.views.tagslist', {}, 'tags_list'),

    (r'archive/(?P<month>\d+)/(?P<cur_page>\d+)/$',  'apps.videoblog.views.videolist', {'tag': None}, 'video_list_page'),
    (r'tag/(?P<tag>[\w ^/\-]+)/page-(?P<cur_page>\d+)/$', 'apps.videoblog.views.videolist', {'month': None}, 'video_list_page'),
    (r'page/(?P<cur_page>\d+)/$', 'apps.videoblog.views.videolist', {'tag': None, 'month': None}, 'video_list_page'),

    (r'feedback/$', 'apps.videoblog.views.feedback', {}, 'feedback'),
    (r'feedback/ok/$', TemplateView.as_view(template_name="feedback_ok.html"), {}, 'feedback_ok'),
    (r'random/$', 'apps.videoblog.views.random_video', {}, 'random'),
    (r'rss/$', LatestEntriesFeed(),{},'rss'),
    
)

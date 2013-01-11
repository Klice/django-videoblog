# -*- coding: utf-8 -*-
from django import template
from django.template.loader import get_template
from django.template import Context
from django.template.defaultfilters import stringfilter
from videoblog.models import Video
import datetime
import itertools

register = template.Library()


@register.filter
@stringfilter
def cutend(value, arg):
    return value[-eval(arg):]


@register.filter
def rupluralize(value, arg=u"дурак,дурака,дураков"):
    args = arg.split(",")
    if not value:
        return args[2]
    number = abs(int(value))
    a = number % 10
    b = number % 100

    if (a == 1) and (b != 11):
        return args[0]
    elif (a > 1) and (a < 5) and ((b < 10) or (b > 20)):
        return args[1]
    else:
        return args[2]


@register.simple_tag
def video_top():
    vlist = Video.objects.extra(select={'r': 'voters_good - voters_bad'}).order_by('-r', '-views')[:10]
    t = get_template('video_top_left.html')
    return t.render(Context({'videos': vlist}))


@register.simple_tag
def showvideo_preview(video):
    if video.hoster == "xhamster.com":
        t = get_template('videos/preview_xhamster.html')
        return t.render(Context({'video': video}))
    if video.hoster == "www.empflix.com":
        t = get_template('videos/preview_empflix.html')
        return t.render(Context({'video': video}))
    if video.hoster == "www.tube8.com":
        t = get_template('videos/preview_tube8.html')
        return t.render(Context({'video': video}))
    if video.hoster == "vk.com":
        t = get_template('videos/preview_vk.html')
        return t.render(Context({'video': video}))
    if video.hoster == "www.xvideos.com":
        t = get_template('videos/preview_xvideos.html')
        return t.render(Context({'video': video}))
    if video.hoster == "www.eroprofile.com":
        t = get_template('videos/preview_eroprofile.html')
        return t.render(Context({'video': video}))
    if video.hoster == "amazon":
        t = get_template('videos/preview_amazon.html')
        return t.render(Context({'video': video}))

@register.simple_tag
def showrel(video, num=5):
    vids = video.GetRel()
    top = dict(itertools.islice(dict(vids).iteritems(), num))
    video_list = []
    for vid in top.keys():
        video_list.append(vid)
    videos = Video.objects.in_bulk(video_list)
    if len(videos) < num:
        num_add = num - len(videos)
        rnd = Video.objects.all().order_by('?')[:num_add]
    else:
        rnd = []
    result = []
    for v in videos.keys():
        result.append(videos[v])
    result = list(itertools.chain(result, rnd))
    t = get_template('video_top.html')
    return t.render(Context({'videos': result}))


@register.simple_tag
def showvideo(video):
    if video.hoster == "xhamster.com":
        t = get_template('videos/video_xhamster.html')
        return t.render(Context({'video': video}))
    if video.hoster == "www.empflix.com":
        t = get_template('videos/video_empflix.html')
        return t.render(Context({'video': video}))
    if video.hoster == "vk.com":
        t = get_template('videos/video_vk.html')
        return t.render(Context({'video': video}))
    if video.hoster == "www.tube8.com":
        from urlparse import urlparse
        t = get_template('videos/video_tube8.html')
        url = urlparse(video.url)
        em_url = "http://" + url.netloc + "/embed" + url.path
        return t.render(Context({'video': video, 'em_url': em_url}))
    if video.hoster == "www.xvideos.com":
        t = get_template('videos/video_xvideos.html')
        return t.render(Context({'video': video}))
    if video.hoster == "www.eroprofile.com":
        t = get_template('videos/video_eroprofile.html')
        return t.render(Context({'video': video}))
    if video.hoster == "amazon":
        t = get_template('videos/video_amazon.html')
        return t.render(Context({'video': video}))

@register.simple_tag
def archive():
    videos = Video.objects.filter().order_by('-date')
    now = datetime.datetime.now()

    video_dict = {}
    for i in range(videos[0].date.year, videos[len(videos) - 1].date.year - 1, -1):
        video_dict[i] = {}
        for month in range(1, 13):
            video_dict[i][month] = {'date': '', 'count': 0}

    for event in videos:
        video_dict[event.date.year][event.date.month]['count'] += 1
        video_dict[event.date.year][event.date.month]['date'] = event.date

    #this is necessary for the years to be sorted
    event_sorted_keys = list(reversed(sorted(video_dict.keys())))
    video_list = []

    for key in event_sorted_keys:
        adict = {key: video_dict[key]}
        video_list.append(adict)

    t = get_template('archive.html')
    c = Context({'now': now, 'video_list': video_list})
    return t.render(c)


@register.simple_tag
def paginator(cur_page, pages, month=0):
    t = get_template('paginator.html')
    return t.render(Context({'cur_page': cur_page, 'pages': pages, 'month': month}))

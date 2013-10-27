# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from apps.videoblog.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from tagging.models import TaggedItem, Tag
import json
from django.views.decorators.cache import cache_page
import random
from apps.videoblog.forms import FeedbackForm
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('feedback_ok'))
    else:
        form = FeedbackForm(initial={'ip': get_client_ip(request)})

    return render_to_response('feedback.html', locals(), RequestContext(request))


@cache_page(10 * 60 * 60)
def tagslist(request):
    tags = Tag.objects.usage_for_model(Video, counts=True, filters=dict(sites__id__exact=get_current_site(request).id))
    return render_to_response('tagslist.html', locals(), RequestContext(request))


@cache_page(3 * 60 * 60)
def videolist(request, cur_page=1, month=None, tag=None):
    r = random.randint(1, 3)
    if month > 0:
        paginator = Paginator(Video.on_site.filter(date__month=month), 10)
    else:
        paginator = Paginator(Video.on_site.all(), 10)
    if tag is not None:
        # f = TaggedItem.objects.get_by_model(Video.on_site.all(), list(tag))
        paginator = Paginator(TaggedItem.objects.get_by_model(Video.on_site.all(), tag + ','), 10)
    curpage = paginator.page(cur_page)
    # raise ValueError
    videos = curpage.object_list
    return render_to_response('videolist.html', locals(), RequestContext(request))


# @user_passes_test(lambda u: u.has_perm('video.can_add'))
def Add_Video_URL(request):
    # import pdb; pdb.set_trace()
    if request.method == 'GET':
        try:
            video = Video(url=request.GET["url"])
            video.save()
            response = HttpResponse()
            response.write(u"Готово")
            return response
        except AttributeError:
            pass
    return HttpResponse(status=400)


def Add_Video_Amazon_URL(request):
    # import pdb; pdb.set_trace()
    if request.method == 'GET':
        try:
            video = Video(
                url='http://candybox.peegirl.ru/movie/' + request.GET["id"],
                video_id=request.GET["id"],
                hoster="amazon",
                name=request.GET["filename"]
            )
            video.save()
            response = HttpResponse()
            response.write(u"Готово")
            return response
        except AttributeError:
            pass
    return HttpResponse(status=400)

# @cache_page(3 * 60 * 60)
def detail_video(request, video_id, name):
    video = get_object_or_404(Video, pk=video_id)
    cache_time=10800
    return render_to_response('videodetail.html', locals(),  RequestContext(request))

def video_count(request, video_id):
    user_viewed = request.session.get('video_viewed')
    last_view = request.session.get('last_view')
    if not user_viewed:
        user_viewed = []
    if not video_id in user_viewed:
        user_viewed.append(video_id)
        video = get_object_or_404(Video, pk=video_id)
        video.add_view()
    if last_view:
        if last_view.pk != video_id:
            video = get_object_or_404(Video, pk=video_id)
            try:
                viewstat, created = ViewStats.objects.get_or_create(video_from=last_view, video_to=video, site=get_current_site(request))
            except ViewStats.MultipleObjectsReturned:
                viewstat = ViewStats.objects.filter(Q(video_from=last_view)&Q(video_to=video)&Q(site=get_current_site(request)))[0]

            viewstat.views += 1
            viewstat.save()

    # raise ValueError
    request.session['last_view'] = video
    request.session['video_viewed'] = user_viewed
    return HttpResponse("OK")


@user_passes_test(lambda u: u.has_perm('video.can_delete'))
def delete_video(request, id):
    get_object_or_404(Video, pk=id).delete()
    try:
        backurl = request.GET["backurl"]
    except MultiValueDictKeyError:
        backurl = '/'
    return HttpResponseRedirect(backurl)


def random_video(request):
    random_video = Video.on_site.filter(sites__id__exact=get_current_site(request).id).order_by('?')[0]
    return HttpResponseRedirect(random_video.get_absolute_url())



@user_passes_test(lambda u: u.has_perm('video.can_change'))
def edit_video_desc(request, id):
    video = get_object_or_404(Video, pk=id)
    try:
        video.desc = request.POST["text"]
        video.save()
    except MultiValueDictKeyError:
        pass
    return HttpResponse(video.desc)


@user_passes_test(lambda u: u.has_perm('video.can_change'))
def edit_video_tags(request, id):
    video = get_object_or_404(Video, pk=id)
    try:
        video.tags = request.POST["tags"]
        video.save()
    except MultiValueDictKeyError:
        pass
    return HttpResponse(video.tags)


def video_vote(request, id, res):
    if request.is_ajax():
        try:
            video_voting = json.loads(request.COOKIES.get('video_voting'))
        except (ValueError, TypeError):
            video_voting = {}

        video = get_object_or_404(Video, pk=id)
        try:
            res_old = video_voting[id]
        except KeyError:
            video.voters += 1
            res_old = 0

        if res > 0:
            if res_old == -1:
                video.voters_bad -= 1
            if res_old != 1:
                video.voters_good += 1
            video_voting[id] = 1
        else:
            if res_old == 1:
                video.voters_good -= 1
            if res_old != -1:
                video.voters_bad += 1
            video_voting[id] = -1
        video.save()
        response_data = {}
        response_data['voters'] = video.voters
        response_data['voters_bad'] = video.voters_bad
        response_data['voters_good'] = video.voters_good
        response = HttpResponse(json.dumps(response_data), mimetype="application/json")
        response.set_cookie('video_voting', json.dumps(video_voting))

        return response
    else:
        return HttpResponse(status=400)

# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from videoblog.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

def videolist(request, cur_page = 1, month=0):
	if month > 0:
		paginator = Paginator(Video.objects.filter( date__month = month ), 10)
	else:
		paginator = Paginator(Video.objects.all(), 10)
	curpage = paginator.page(cur_page)
	videos = curpage.object_list
	return render_to_response('videolist.html',locals(),  RequestContext(request))

# @user_passes_test(lambda u: u.has_perm('video.can_add'))
def Add_Video_URL(request):
	# import pdb; pdb.set_trace()
	if request.method == 'GET':
		try:
			video = Video(url = request.GET["url"])
			video.save()
			response = HttpResponse()
			response.write(u"Готово")
			return response
		except AttributeError:
			pass
	return HttpResponse(status=400)

def detail_video(request, video_id, name):
	video = get_object_or_404(Video, pk = video_id)
	user_viewed = request.session.get('video_viewed')
	last_view = request.session.get('last_view')
	if not user_viewed:
		user_viewed = []
	if not video_id in user_viewed:
		user_viewed.append(video_id)
		video.add_view()
	if last_view:
		if last_view != video:
			viewstat, created = ViewStats.objects.get_or_create(video_from=last_view, video_to=video)
			viewstat.views += 1
			viewstat.save()
	# raise ValueError
	request.session['last_view'] = video
	request.session['video_viewed'] = user_viewed

	return render_to_response('videodetail.html',locals(),  RequestContext(request))

@user_passes_test(lambda u: u.has_perm('video.can_delete'))
def delete_video(request, id):
	video = get_object_or_404(Video, pk = id).delete()
	try:
		backurl = request.GET["backurl"]
	except MultiValueDictKeyError:
		backurl = '/'
	return HttpResponseRedirect(backurl)
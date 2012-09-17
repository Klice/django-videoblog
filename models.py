# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
import urllib2
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from xml.dom.minidom import parseString





class Video (models.Model):
	url = models.URLField(max_length=255,verbose_name=(u"URL видео"))
	video_id = models.CharField(max_length=255,verbose_name=(u"ID видео"),blank=True)
	hoster = models.CharField(max_length=255,verbose_name=(u"Адрес хостинга"),blank=True)
	player = models.CharField(max_length=255,verbose_name=(u"Ссылка плеера"),blank=True)
	name = models.CharField(max_length=255,verbose_name=(u"Название"),blank=True)
	desc = models.TextField(verbose_name=(u"Описание"),blank=True)
	date = models.DateTimeField(auto_now_add=True)
	thumb = models.ImageField(upload_to='thumbs/',verbose_name=(u"Картинка"),blank=True)
	views = models.IntegerField(verbose_name=(u"Количество просмотров"),default=0)

	def save(self, *args, **kwargs):
		from urlparse import urlparse
		import re
		url = urlparse(self.url)
		if not self.hoster:
			self.hoster = url.netloc

		if not self.video_id:
			if self.hoster == 'xhamster.com':
				p = re.compile('/movies/(?P<id>\d+)/')
				self.video_id = p.search(url.path).group("id")
			if self.hoster == 'www.empflix.com':
				p = re.compile('\-(?P<id>\d+)\.html')
				self.video_id = p.search(url.path).group("id")
			if self.hoster == 'www.tube8.com':
				p = re.compile('/(?P<id>\d+)/$')
				self.video_id = p.search(url.path).group("id")
			if self.hoster == 'vk.com':
				p = re.compile('/video(?P<id>[0-9_]+)$')
				self.video_id = p.search(url.path).group("id")
			if self.hoster == 'www.xvideos.com':
				p = re.compile('/video(?P<id>[0-9_]+)/')
				self.video_id = p.search(url.path).group("id")


		if not self.name:
			if self.hoster == 'xhamster.com':
				p = re.compile('/movies/\d+/(?P<name>.+)\.html$')
				self.name = p.search(url.path).group("name").replace('_' ,' ')
			if self.hoster == 'www.empflix.com':
				p = re.compile('/videos/(?P<name>.+)\-\d+\.html')
				self.name = p.search(url.path).group("name").replace('-' ,' ')
			if self.hoster == 'www.tube8.com':
				p = re.compile('/(?P<name>[a-zA-Z- ]+)/\d+/$')
				self.name = p.search(url.path).group("name").replace('-' ,' ')
			if self.hoster == 'www.xvideos.com':
				p = re.compile('/video[0-9_]+/(?P<name>[a-zA-Z-_ ]+)$')
				self.name = p.search(url.path).group("name").replace('_' ,' ')

		if not self.thumb or not self.name:
			if self.hoster == 'vk.com':
				from random import randrange
				import md5
				import time
				import simplejson

				code = '74907dd9c31dca9adb'

				url = 'http://api.vk.com/api.php'
				param = {}
				param['api_id'] = '3112017'
				param['format'] = 'json'
				# param['method'] = 'getUserSettings'
				# param['uid'] = '68037910'
				param['random'] = str(randrange(10000, 99999))
				param['method'] = 'video.get'
				param['v'] = '3.0'
				secret = 'gLTHX532pNf1hBIDbzHt'
				param['access_token'] = '074610c05304e43203483dd639036741870034803483dc693809ec1ac215478'
				param['videos'] = self.video_id
				param['timestamp'] = str(time.time())
				keylist = param.keys()
				keylist.sort()
				sig_str = ''
				for key in keylist:
					sig_str += key + '=' + param[key]
				sig_str+=secret
				param['sig'] = md5.new(sig_str).hexdigest()
				url_param = ''
				for key in sorted(param.keys()):
					url_param += key + '=' + param[key] + '&'
				url+='?' + url_param
				page = urllib2.urlopen(url).read()
				data = simplejson.loads(page)
				# try:
				# import pdb; pdb.set_trace()
				if not self.name:
					self.name = data['response'][1]['title']
				if not self.thumb:
					img_temp = NamedTemporaryFile()
					img_temp.write(urllib2.urlopen(data['response'][1]['image']).read())
					img_temp.flush()
					self.thumb.save(self.video_id + '.jpeg', File(img_temp))
				if not self.desc:
					self.desc = data['response'][1]['description']
				if not self.player:
					self.player= data['response'][1]['player']


		if not self.thumb:
			if self.hoster == 'www.tube8.com':
				page = urllib2.urlopen(self.url).read()
				# import pdb; pdb.set_trace()
				p = re.compile('\"image_url\":\"(?P<thumb>[^"]+)\"')
				url = p.search(page).group("thumb").replace('\\' ,'')
				img_temp = NamedTemporaryFile()
				img_temp.write(urllib2.urlopen(url).read())
				img_temp.flush()
				self.thumb.save(self.video_id + '.jpeg', File(img_temp))
			if self.hoster == 'www.empflix.com':
				page = urllib2.urlopen(self.url).read()
				p = re.compile('flashvars.config \= escape\(\"(?P<cfg_url>[^"]+)\"\);')
				cfg = urllib2.urlopen(p.search(page).group("cfg_url")).read()
				dom = parseString(cfg)
				url = dom.getElementsByTagName("startThumb")[0].firstChild.nodeValue
				# import pdb; pdb.set_trace()
				img_temp = NamedTemporaryFile()
				img_temp.write(urllib2.urlopen(url).read())
				img_temp.flush()
				self.thumb.save(self.video_id + '.jpeg', File(img_temp))
			if self.hoster == 'www.xvideos.com':
				page = urllib2.urlopen(self.url).read()
				p = re.compile('flashvars\=.*url_bigthumb\=(?P<img_url>[^&]+)')
				img = urllib2.urlopen(p.search(page).group("img_url")).read()
				# import pdb; pdb.set_trace()
				img_temp = NamedTemporaryFile()
				img_temp.write(img)
				img_temp.flush()
				self.thumb.save(self.video_id + '.jpeg', File(img_temp))


		super(Video, self).save(*args, **kwargs)

	def get_absolute_url(self):
		# import pdb; pdb.set_trace()
		import pytils  
		return reverse('detail_video', kwargs={'video_id': self.id, 'name': pytils.translit.slugify(self.name),})

	def add_view(self):
		self.views+=1
		self.save()

	class Meta:
		ordering = ('-date',)
		get_latest_by = 'date'
		verbose_name_plural = 'видео'

	def __unicode__(self):
		return "%s" % self.name


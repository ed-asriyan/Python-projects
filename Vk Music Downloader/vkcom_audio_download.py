# -*- coding: utf-8 -*-
'''
Скрипт для скачивания музыки с сайта vk.com

Запуск:
python vkcom_audio_download.py [...]

Принцип работы:
Скрипт проверяет сохраненный access_token. Если его нет или срок истек,
то открывается страница в браузере с запросом на доступ к аккаунту.
После подтверждения идет редирект на https://oauth.vk.com/blank.htm#... .
Нужно скопировать весь url, на который вас редиректнуло и вставить его
в консоль скрипта.

Будут запрошены ваши данные приложением с app_id = 3358129
Можно создать свое Standalone-приложение с доступом к аудио здесь:
http://vk.com/editapp?act=create
И заменить APP_ID на ваше.
'''

'''
Edited by Ed Asriyan 2016
Source: https://gist.github.com/st4lk/4708673
'''

import sys
import webbrowser
import pickle
import json
import urllib
import urllib2
import HTMLParser
import re
import os
import urlparse
from datetime import datetime, timedelta

# chars to exclude from filename
AUTH_FILE = '.auth_file'
FORBIDDEN_CHARS = '/\\\?%*:|\'<>!'

# filter for audio track
class AudioFilter:
	max_duration = None

# filter for audio track list
class AudioListFilter:
	offset = 0
	count  = None

# program settings, returns number of advanced readed parameters
class Settings:
	audio_filter	  = AudioFilter()
	audio_list_filter = AudioListFilter()

	# do not download, only show track list
	print_only = False

	download_directory = 'music'
	app_id = '3358129'

	access_token   = None
	expires_in     = None
	user_id        = None
	search_id      = None
	is_force_download = False

	is_empty_invoke = False

	def _handle_arg(self, param, args):
		if param == 'p':
			self.download_directory = unicode(args[0])
			return 1
		elif param == 'c':
			self.audio_list_filter.count = int(args[0])
			return 1
		elif param == 'o':
			self.audio_list_filter.offset = int(args[0])
			return 1
		elif param == 'print':
			self.print_only = True
			return 0
		elif param == 'f':
			self.is_force_download = True
			return 0
		elif param == 'userid':
			self.search_id = int(args[0])
			return 1
		elif param == 'd':
			self.audio_filter.max_duration = int(args[0])
			return 1
		# elif param == 'appid':
		# 	self.appid = arg[0]
		# 	return 1
		# elif param == 'token':
		# 	self.access_token = arg[0]
		# 	return 1

		return 0

	def __init__(self, args):
		self.is_empty_invoke = not len(args)
		i = 0;
		while i < len(args):
			i += 1 + self._handle_arg(args[i][1:], args[i + 1:])

# represents audio track from vk.com
class VkAudio:
	def __init__(self, audio_obj):
		self.artist   = unicode(audio_obj['artist'])
		self.title	  = unicode(audio_obj['title'])
		self.duration = int(audio_obj['duration'])
		self.url      = unicode(audio_obj['url'])

	def to_string(self):
		result = (unicode(self.artist) + u' — ' + unicode(self.title))
		for c in FORBIDDEN_CHARS:
			result = result.replace(c, '')
		return result

# checks audio by filter
def check_audio(audio, filter):
	return not filter.max_duration or audio.duration <= filter.max_duration

# returns filtered audio list
def filter_audio_list(audio_list, filter_audio_list, filter_audio):
	begin = filter_audio_list.offset if filter_audio_list.offset else 0
	end   = filter_audio_list.count + begin if filter_audio_list.count else len(audio_list)

	return [ audio for audio in audio_list[begin:end] if check_audio(audio, filter_audio) ]


# reads auth information from file
def read_saved_auth_params():
	access_token = None
	user_id      = None
	expires_in   = None
	try:
		with open(AUTH_FILE, 'rb') as pkl_file:
			token = pickle.load(pkl_file)
			expires = pickle.load(pkl_file)
			uid = pickle.load(pkl_file)
		if datetime.now() < expires:
			access_token = token
			user_id      = uid
			expires_in   = expires 
	except IOError:
		pass
	return access_token, user_id, expires_in

# saves auth information to file
def save_auth_params(settings):
	with open(AUTH_FILE, 'wb') as output:
		pickle.dump(settings.access_token, output)
		pickle.dump(settings.expires_in, output)
		pickle.dump(settings.user_id, output)


# authorizes & writes auth information to settings
def auth_to_settings(settings):
	auth_url = ('https://oauth.vk.com/authorize?client_id={app_id}'
				'&scope=audio&redirect_uri=http://oauth.vk.com/blank.html'
				'&display=page&response_type=token'.format(app_id=settings.app_id))
	webbrowser.open_new_tab(auth_url)
	redirected_url = raw_input('Paste here url you were redirected:\n')
	aup = urlparse.parse_qs(redirected_url)
	aup['access_token'] = aup.pop('https://oauth.vk.com/blank.html#access_token')

	settings.access_token = aup['access_token'][0]
	settings.expires_in   = datetime.now() + timedelta(seconds=int(aup['expires_in'][0]))
	settings.user_id      = aup['user_id'][0]

# stores auth info
def restore_to_settings(settings):
	settings.access_token, settings.user_id, settings.expires_in = read_saved_auth_params()
	if not settings.access_token or not settings.user_id or not settings.expires_in:
		auth_to_settings(settings)


def get_audio_tracks(settings):
	url = ('https://api.vkontakte.ru/method/audio.get.json?'
		'uid={uid}&access_token={atoken}'.format(
			uid=(settings.search_id if settings.search_id else settings.user_id), atoken=settings.access_token))
	audio_get_page = urllib2.urlopen(url).read()
	audio_list_obj = json.loads(audio_get_page)['response']

	return [ VkAudio(audio_obj) for audio_obj in audio_list_obj ]


def download_track(url, path):
	urllib.urlretrieve(url, path)


def main():
	settings = Settings(sys.argv[1:])

	if settings.is_empty_invoke:
		print 'Parameters:'
		print '-p      - path to saving directory'
		print '-c      - number of tracks'
		print '-o      - track list offset'
		print '-f      - download track anyway (if it exists)'
		print '-userid - id of track list owner'
		print '-print  - do not download tracks (only print to console)'
		print '-d      - the highest border of song duration to download'
		print '[any_other_key] - to use default parameters.'

		return

	if not settings.access_token or not settings.user_id or not settings.expires_in:
		restore_to_settings(settings)
		save_auth_params(settings)

	print 'Getting track list...'
	tracks = get_audio_tracks(settings)
	tracks = filter_audio_list(tracks, settings.audio_list_filter, settings.audio_filter)

	if settings.download_directory and not os.path.exists(settings.download_directory):
		os.makedirs(settings.download_directory)

	for index, track in enumerate(tracks):
		name = track.to_string()
		save_path = settings.download_directory + u'/' + name + u'.mp3'

		if settings.is_force_download or not os.path.exists(save_path):
			print u'{:d}/{:d}: {:60s} ({:d} s)'.format(index + 1, len(tracks), name, track.duration)
			
			if not settings.print_only:
				download_track(track.url, save_path)
			# print t
		# else:
		# 	print '{0}/{1} Skipping {2}'.format(index + 1, t_count, t_name.encode('ascii', 'replace'))

	print 'Done.'


if __name__ == '__main__':
	main()

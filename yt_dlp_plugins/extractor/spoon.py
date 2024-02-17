from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import UserNotLive
from yt_dlp.utils import traverse_obj
from datetime import datetime

class SpoonLiveIE(InfoExtractor):
    _WORKING = True
    _VALID_URL = r'https://www.spooncast.net/jp/live/@(?P<id>.+)'

    def _real_extract(self, url):
        self.to_screen('spoon url "%s" successfully captured by SpoonLiveIE' % url)
        uploader_id = self._match_id(url)
        profile_url = 'https://jp-api.spooncast.net/profiles/%s/meta/' % uploader_id
        self.to_screen('get live id from user profile url: "%s"' % profile_url)
        webpage = self._download_webpage(profile_url, uploader_id)

        self.to_screen('dump profile meta json\n------\n"%s"\n------\n' % webpage)

        profile_js_data = self._parse_json(webpage, uploader_id)

        current_live_id = traverse_obj(profile_js_data, ('results', 0, 'current_live_id'))

        self.to_screen('current live id: "%s"' % str(current_live_id))

        if not current_live_id:
            raise UserNotLive(video_id=uploader_id)

        current_live_id = str(current_live_id) # avoid type warning

        live_info_url = 'https://jp-api.spooncast.net/lives/%s/' % current_live_id

        self.to_screen('live info url: "%s"' % live_info_url)

        webpage = self._download_webpage(live_info_url, current_live_id)

        video_js_data = self._parse_json(webpage, current_live_id)

        thumbnail = traverse_obj(video_js_data, ('results', 0, 'img_url'))

        description = traverse_obj(video_js_data, ('results', 0, 'welcome_message'))

        title = traverse_obj(video_js_data, ('results', 0, 'title'))

        hls_url = traverse_obj(video_js_data, ('results', 0, 'url_hls'))

        if not hls_url:
            raise UserNotLive(video_id=uploader_id)

        self.to_screen('m3u8 url: "%s"' % hls_url)

        m3u8_url = hls_url

        formats = self._extract_m3u8_formats(
            m3u8_url, current_live_id, ext='mp4', m3u8_id='hls',
            live=True)

        infodict = {
            'formats': formats,
            '_format_sort_fields': ('source', ),
        }

        base_dict = {
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'uploader_id': uploader_id,
            'is_live': True,
        }

        return {
            'id': current_live_id,
            **base_dict,
            **infodict,
        }

class SpoonCastIE(InfoExtractor):
    _WORKING = True
    _VALID_URL = r'https://www.spooncast.net/jp/cast/(?P<id>\d+)'

    def _real_extract(self, url):
        video_id = self._match_id(url)

        if video_id is None:
            self._error_or_warning('load video info fail')
            
        video_info_url = 'https://jp-api.spooncast.net/casts/%s/' % video_id

        webpage = self._download_webpage(video_info_url, video_id)
        video_js_data = self._parse_json(webpage, video_id)
        img_url = traverse_obj(video_js_data, ('results', 0, 'img_url'))
        voice_url = traverse_obj(video_js_data, ('results', 0, 'voice_url'))
        nickname = traverse_obj(video_js_data, ('results', 0, 'author', 'nickname'))
        title = traverse_obj(video_js_data, ('results', 0, 'title'))
        description = traverse_obj(video_js_data, ('results', 0, 'welcome_message'))

        # 2023-01-19T13:00:18.828274Z
        created = datetime.strptime(
            traverse_obj(video_js_data, ('results', 0, 'created')),
            '%Y-%m-%dT%H:%M:%S.%fZ')

        self.to_screen(created)

        if voice_url is None:
            self._error_or_warning('not found m4a url')
        
        return {
            'id': str(video_id),
            'title': title,
            'description': description,
            'formats': [{'url':voice_url, 'format_id': 'http-mp4'}],
            'thumbnail': img_url,
            'uploader': nickname,
            'timestamp': created.timestamp(),
            }

            

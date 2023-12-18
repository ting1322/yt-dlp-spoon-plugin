from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import UserNotLive
from yt_dlp.utils import traverse_obj

class SpoonLiveIE(InfoExtractor):
    _WORKING = True
    _VALID_URL = r'https://www.spooncast.net/jp/live/@(?P<id>.+)'

    def _real_extract(self, url):
        self.to_screen('URL "%s" successfully captured' % url)
        uploader_id = self._match_valid_url(url).groups()
        profile_url = 'https://jp-api.spooncast.net/profiles/%s/meta/' % uploader_id
        self.to_screen(profile_url)
        webpage = self._download_webpage(profile_url, uploader_id)

        profile_js_data = self._parse_json(webpage, uploader_id)

        current_live_id = traverse_obj(profile_js_data, ('results', 0, 'current_live_id'))

        self.to_screen('current live id %s' % current_live_id)

        if not current_live_id:
            raise UserNotLive(video_id=uploader_id)

        live_info_url = 'https://jp-api.spooncast.net/lives/%s/' % current_live_id

        self.to_screen('get info page %s' % live_info_url)
        
        webpage = self._download_webpage(live_info_url, current_live_id)

        video_js_data = self._parse_json(webpage, current_live_id)

        thumbnail = traverse_obj(video_js_data, ('results', 0, 'img_url'))

        description = traverse_obj(video_js_data, ('results', 0, 'welcome_message'))

        title = traverse_obj(video_js_data, ('results', 0, 'title'))

        hls_url = traverse_obj(video_js_data, ('results', 0, 'url_hls'))

        if not hls_url:
            raise UserNotLive(video_id=uploader_id)

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

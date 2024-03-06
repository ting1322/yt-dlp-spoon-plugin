from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import UserNotLive
from yt_dlp.utils import traverse_obj
from datetime import datetime

class ChzzkLiveIE(InfoExtractor):
    _WORKING = True
    _VALID_URL = r'https://chzzk.naver.com/live/(?P<id>.+)'

    def _real_extract(self, url):
        self.to_screen('chzzk url "%s" successfully captured by ChzzkLiveIE' % url)
        channel_id = self._match_id(url)
        live_info_url = 'https://api.chzzk.naver.com/service/v2/channels/%s/live-detail' % channel_id
        self.to_screen('get live-detail ' + live_info_url)
        webpage = self._download_webpage(live_info_url, channel_id)
        self.to_screen('get live-detail\n---\n%s\n---' % webpage)
        live_detail_js_data = self._parse_json(webpage, channel_id)
        live_status = traverse_obj(live_detail_js_data, ('content', 'status'))
        channel_name = traverse_obj(live_detail_js_data, ('content', 'channel', 'channelName'))
        title = traverse_obj(live_detail_js_data, ('content', 'liveTitle'))
        thumbnail = traverse_obj(live_detail_js_data, ('content', 'liveImageUrl'))
        if not live_status or live_status != 'OPEN':
            raise UserNotLive(video_id=channel_id)
        livePlaybackText = traverse_obj(live_detail_js_data, ('content', 'livePlaybackJson'))
        self.to_screen('get PlaybackText\n---\n%s\n---' % webpage)

        livePlayback = self._parse_json(livePlaybackText, channel_id)

        m3u8_url = traverse_obj(livePlayback, ('media', 0, 'path'))

        current_live_id = traverse_obj(livePlayback, ('meta', 'videoId'))

        self.to_screen('m3u8 url: ' + m3u8_url)

        formats = self._extract_m3u8_formats(
            m3u8_url, current_live_id, ext='mp4', m3u8_id='hls',
            live=True)

        return {
            'id': current_live_id,
            'title': title,
            'thumbnail': thumbnail,
            'uploader_id': channel_name,
            'upload_date': datetime.today().strftime('%Y%m%d'),
            'is_live': True,
            'formats': formats,
        }

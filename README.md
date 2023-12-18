yt-dlp plugin for `https://www.spooncast.net/jp/live/`

這邊只負責把 spoon 的 m3u8 網址抓出來，剩下的事情 yt-dlp + ffmpeg 會處理。

# Install

ref https://github.com/yt-dlp/yt-dlp#installing-plugins

## windows:

1. 檔案總管網址打 `%APPDATA%`
2. 下載檔案 [spoon.py](yt_dlp_plugins/extractor/spoon.py)
3. 檔案放好 `C:\Users\<USER_NAME>\AppData\Roaming\yt-dlp-plugins\spoon\yt_dlp_plugins\extractor\spoon.py`
   路徑很重要，一層都不能少！
3. 試著找一個 spoon 的網址，給 yt-dlp 下參數 `yt-dlp -F --verbose https://www.spooncast.net/jp/live/@xxxxx`
   如果能抓到直播的格式，那就正確了

## 疑難排解

1. 觀察 `--verbose` 的輸出，有沒有抓到 `yt-dlp-plugins` 目錄
2. 確定你有一層不漏，一字不改的建好目錄結構

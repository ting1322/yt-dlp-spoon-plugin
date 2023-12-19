yt-dlp plugin for `https://www.spooncast.net/jp/live/`

把這個 repo 的檔案下載，放到正確的地方，[yt-dlp](https://github.com/yt-dlp/yt-dlp) 就能下載 spoon 的影片。

這邊只負責把 spoon 的 m3u8 網址抓出來，剩下的事情 yt-dlp + ffmpeg 會處理。

# Install

目錄有很多種選擇，參考： https://github.com/yt-dlp/yt-dlp#installing-plugins

## Git 安裝

1. 首先你要有 Git
2. `mkdir $HOME/.config/yt-dlp/plugins`
3. `cd $HOME/.config/yt-dlp/plugins`
4. `git clone https://github.com/ting1322/yt-dlp-spoon-plugin.git`

未來升級 plugin 就普通的 `git pull --rebase`

windows 的話目錄是 `C:\Users\<USER_NAME>\AppData\Roaming\yt-dlp-plugins\`
在這邊 git clone。

## windows 手動安裝:

給前一段看不懂的人。

1. 檔案總管網址打 `%APPDATA%`
2. 下載檔案 [spoon.py](yt_dlp_plugins/extractor/spoon.py)
3. 檔案放好 `C:\Users\<USER_NAME>\AppData\Roaming\yt-dlp-plugins\spoon\yt_dlp_plugins\extractor\spoon.py`
   路徑很重要，一層都不能少！
3. 試著找一個 spoon 的網址，給 yt-dlp 下參數 `yt-dlp -F --verbose https://www.spooncast.net/jp/live/@xxxxx`
   如果能抓到直播的格式，那就正確了

## 疑難排解

1. 觀察 `--verbose` 的輸出，有沒有抓到 `yt-dlp-plugins` 目錄
2. 確定你有一層不漏，一字不改的建好目錄結構
3. 確定你給的網址是 jp 版的 spoon。另外也有 kr 版，這邊不支援。
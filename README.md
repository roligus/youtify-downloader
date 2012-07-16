Youtify playlist downloader
---------------------------

Requirements:
-------------
* [Python](http://python.org/download/) 2.5 or greater 
* [FFmpeg](http://ffmpeg.org/) binaries
    * [Windows: binaries](http://ffmpeg.zeranoe.com/builds/)
    * [OSX: The lazy way](http://hints.macworld.com/article.php?story=20061220082125312)
    * [OSX: How to compile](http://hunterford.me/compiling-ffmpeg-on-mac-os-x/)

How to use:
-----------
How to download all playlists for a profile:
    > python main.py <username>

Download only a specific playlist:
    > python main.py <username> <playlistid>

Example:
    python main.py lars_ulrich
    python main.py lars_ulrich 123456
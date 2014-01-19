#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
from threading import Thread
from misc import *
import httplib
import sys
import urllib2
import string
import locale
import os
import subprocess
import math
import time

class TrackDownloader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.track = None
        self.path = None
        self.running = False
    
    def download(self, url, title, path):
        CHUNK = 16 * 1024
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.56 Safari/536.5'}
        try:
            request = urllib2.Request(url, None, headers)
            response = urllib2.urlopen(request)
            read = 0
            length = response.info()['Content-Length']
            
            try:
                file = open(path, 'wb')
            except err:
                print err
                return
            while True:
                chunk = response.read(CHUNK)
                if not chunk: break
                file.write(chunk)
                read += len(chunk)
            response.close()
            file.close()
            time.sleep(0.5)
        except (urllib2.HTTPError, ), err:
            log(title + " failed to download")
            time.sleep(1)

    def convert_to_mp3(self, path, title):
        out_path = path + '.mp3'
        meta = getMetaData(title)
        cmd = ['ffmpeg', 
            '-y', '-vn',
            '-shortest',
            '-i', '\"' + path + '\"', 
            '-acodec', 'libmp3lame', '-aq', '2',
            '-metadata title="' + meta['title'] + '"',
            '-metadata artist="' + meta['artist'] + '"',
            '-v', 'error', 
            '\"' + out_path + '\"']
        #log("converting " + title)
        try:
            #subprocess.call(cmd)
            os.system(' '.join(cmd))
        except:
            gc.collect()
            return
        os.remove(path)
        time.sleep(0.5)

    def save_track(self, track, dir):
        SOUNDCLOUD_API_KEY = '2eaed1ea75621614e69a631ca8c42b13'
        
        
        # create path [user]/[playlist]/[track].mp3
        title = clean_filename(track['title'])
        path = os.path.join(dir, title + u'.mp3')
        if os.path.exists(path):
            return
        
        if track['videoId'] is None:
            return
        
        if 'type' not in track or track['type'] == 'youtube':
            path = os.path.join(dir, title)
            cmd = ['python', 'youtube-dl', 'http://www.youtube.com/watch?v=' + track['videoId'], '-q', '-o', path]
            #cmd = ['http://www.youtube.com/watch?v=' + track['videoId'], '-q', '-o', path]
            try:
                #log("downloading " + title)
                subprocess.call(cmd, shell=False)
                #YouTubeDownloader(cmd, self.reporter, self.channel)
            except:
                #gc.collect() # easier than to track the leaks in youtube-dl :s
                log(title + " failed to download (YouTubeDownloader)")
                time.sleep(1)
            
            if os.path.exists(path):
                self.convert_to_mp3(path, title)
            else:
                log(path + " failed (does not exist)")
                time.sleep(1)
        elif 'type' in track and track['type'] == 'soundcloud':
            url = 'https://api.soundcloud.com/tracks/' + str(track['videoId']) + '/stream?client_id=' + SOUNDCLOUD_API_KEY
            self.download(url, title, path)
        elif 'type' in track and track['type'] == 'officialfm':
            id = 0
            try:
                id = int(track['videoId'])
            except:
                log(title + " doesn't have a soundcloud id. " + str(track['videoId']) + " is not an integer.")
                return
            url = 'http://cdn.official.fm/mp3s/' + str(int(math.floor(id / 1000))) + '/' + str(id) + '.mp3'
            self.download(url, title, path)
    
    def run(self):
        if self.track is None or self.path is None:
            return
        self.running = True
        self.save_track(self.track, self.path)
        self.running = False
    
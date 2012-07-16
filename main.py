#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import sys
import urllib2
import simplejson
import string
import os
import subprocess
import signal
import math
import time
from misc import *
from TrackDownloader import TrackDownloader

class YoutifyDownloader():
    def __init__(self, concurrent_threads):
        self.threads = []
        self.max_threads = concurrent_threads
        self.thread_counter = 0
        self.total_tracks = 0
        self.saved_tracks = 0
    
    def remove_dead_threads(self):
        for index in range(len(self.threads) -1, -1, -1):
            if self.threads[index].running == False:
                self.threads[index].join()
                self.threads.pop(index)
    
    def kill_all_threads(self):
        for thread in self.threads:
            if thread is not None:
                thread._Thread__stop()
    
    def find_thread(self):
        while True:
            self.remove_dead_threads()
            if len(self.threads) < self.max_threads:
                self.thread_counter += 1
                thread = TrackDownloader()
                self.threads.append(thread)
                return thread
            time.sleep(0.1)

    def save_playlist(self, playlist, dir):
        # create path [user]/[playlist]
        title = clean_filename(playlist['title'])
        path = os.path.join(dir, title)
        ensure_dir(path)
        log(path)
        
        tracks = simplejson.loads(playlist['videos'])
        for track in tracks:
            title = clean_filename(track['title'])
            track_path = os.path.join(path, title + u'.mp3')
            if not os.path.exists(track_path):
                thread = self.find_thread()
                thread.track = track
                thread.path = path
                thread.start()
            self.saved_tracks += 1
            log((str(self.saved_tracks / self.total_tracks * 100.0) + '% (' + str(self.saved_tracks) + '/' + str(self.total_tracks) + ')').rjust(80))
                    
    def get_user(self, name):
        url = u'http://www.youtify.com/api/users/' + name + u'/playlists'
        request = urllib2.Request(url, None, {})
        try:
            response = urllib2.urlopen(request)
        except (urllib2.HTTPError, ), err:
            if err.code < 500 or err.code >= 600:
                log(err.code)
                raise
        data = response.read()
        response.close()
        playlists = simplejson.loads(data)
        
        # create path [user]/
        path = clean_filename(name)
        ensure_dir(path)
        log(path)
        
        # calc total tracks
        for playlist in playlists:
            self.total_tracks += self.get_nbr_of_tracks(playlist)
        
        for playlist in playlists:
            self.save_playlist(playlist, path)
            print str(self.saved_tracks/self.total_tracks*100.0) + '%'

    def get_playlist(self, name, playlist_id):
        url = u'http://www.youtify.com/api/playlists/' + playlist_id
        request = urllib2.Request(url, None, {})
        try:
            response = urllib2.urlopen(request)
        except (urllib2.HTTPError, ), err:
            if err.code < 500 or err.code >= 600:
                log(err.code)
                raise
        data = response.read()
        response.close()
        playlist = simplejson.loads(data)
        
        # create path [user]/
        path = clean_filename(name)
        ensure_dir(path)
        log(path)
        
        # calc total tracks
        self.total_tracks = self.get_nbr_of_tracks(playlist)
        
        self.save_playlist(playlist, path)

    def get_nbr_of_tracks(self, playlist):
        if 'videos' in playlist:
            return len(playlist['videos'])
        else:
            return 0
    

youtify_downloader = None

def main():
    if len(sys.argv) <= 1:
        print 'usage: python main.py <youtify-username>'
        print 'usage: python main.py <youtify-username> <playlist-id>'
        sys.exit()
    
    threads = 16
    global youtify_downloader
    
    youtify_downloader = YoutifyDownloader(threads)
    
    if len(sys.argv) == 2:
        youtify_downloader.get_user(sys.argv[1])
    
    if len(sys.argv) == 3:
        youtify_downloader.get_playlist(sys.argv[1], sys.argv[2])

def signal_handler(signal, frame):
    print 'killing threads'
    youtify_downloader.kill_all_threads()
    time.sleep(1)
    print 'bye!'
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
	main()

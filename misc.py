#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import os
import subprocess
import re

def clean_filename(f):
    special = [u' ', u'.', u',', u'_', u'-', u'=', u'+', u'#', u'¤', 
        u'%', u'&', u'¨', u'^', u'~', u'(', u')', u'[', u']', 
        u'{', u'}', u'!', u'@', u'£', u'$', u'€', u'´', u'`',
        u'/', u'\\']
    n = u''.join([c for c in f if c.isalpha() or c.isdigit() or c in special])
    
    while n.find(u'  ') >= 0:
        n = n.replace(u'  ', u' ')
    replace = [
        [u'ë', u'e'],
        [u'Ë', u'E'],
        [u'ê', u'e'],
        [u'Ê', u'E'],
        [u'å', u'a'],
        [u'Å', u'A'],
        [u'ä', u'a'],
        [u'Ä', u'A'],
        [u'ö', u'o'],
        [u'Ö', u'O'],
        [u'ô', u'o'],
        [u'Ô', u'O'],
        [u'ø', u'o'],
        [u'Ø', u'O'],
        [u'æ', u'a'],
        [u'Æ', u'A'],
        
        [u'/', u'-'],
        [u'\\', u'-'],
    ]
    for pair in replace:
        n = n.replace(pair[0], pair[1])
    
    n = n.encode('ascii', 'ignore')
    n = n.strip()
    return n
    
def ensure_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)
        
def log(obj, last = False):
    if last:
        sys.stdout.write('\r')
    sys.stdout.flush()
    if type(obj) == type([]):
        for t in obj:
            sys.stdout.write(t.encode('ascii', 'replace'))
            sys.stdout.flush()
    elif type(obj) == type('') or type(obj) == type(u''):
        sys.stdout.write(obj.encode('ascii', 'replace').replace('\n', ''))
        sys.stdout.flush()
    else:
        try:
            print obj
        except:
            return
    if not last:
        sys.stdout.write('\n')
        sys.stdout.flush()

    
def clear():
    os.system(['clear','cls'][os.name == 'nt'])

def getMetaData(title):
    meta = { 'artist': '', 'title': ''}
    strip = [
        u'(official video hd)',
        u'(official video)',
        u'official video hd',
        u'official video hq',
        u'official video',
        u'official lyrics video',
        u'officiell video',
        u'official music video',
        u'official musicvideo',
        u'(official)',
        u'[official]',
        u' 720p',
        u' 1080p',
        u'.wmv',
        u'.mp3',
        u'(videoclip)',
        u'(lyrics)',
        u'w/lyrics',
        u'[lyrics]',
        u'(with lyrics)',
        u'[with lyrics]',
        u'with lyrics',
        u'lyrics on screen',
        u' lyrics',
        u'(text)',
        u'(med text)',
        u'(original)',
        u'[original]',
        u'(cover art)',
        u'[cover art]',
        u'(coverart)',
        u'[coverart]',
        u'[new song]',
        u'(new song)',
        u' p/v',
        u' m/v',
        u'[music]',
        u'(music)',
        u'(ost)',
        u'(ost soundtrack)',
        u' ost soundtrack',
        u' ost ',
        u' high quality',
        u'(high quality)',
        u' best copy',
        u'(best copy)',
        u'[best copy]',
        u'[HD+HQ]',
        u'(HD+HQ)',
        u'[HD HQ]',
        u'(HD HQ)',
        u'[ HD HQ ]',
        u'HD HQ',
        u'- [HQ]',
        u'-[HQ]',
        u'[HQ]',
        u'[HQ',
        u'(HQ)',
        u'-HQ-',
        u'Full HQ',
        u'video HQ',
        u' HQ',
        u'Full HD',
        u'[full]',
        u'(full)',
        u'full video',
        u'full track',
        u'HD version',
        u'- [HD]',
        u'-[HD]',
        u'[HD',
        u'[HD]',
        u'(HD)',
        u'-HD-',
        #u' HD',
        u'video HD',
        u'[Free Download]',
        u' Free Download in description',
        u' Free Download',
        u'[Dubstep]',
        u'(Dubstep)',
        u'[DnB]',
        u'(DnB)',
        u'[Dubstyle]',
        u'(Dubstyle)',
        u'[elektro]',
        u'(elektro)',
        u'[Monstercat Release]',
        u'[Monstercat VIP Release]',
        u'[]',
        u'[ ]',
        u'()',
        u'( )',
    ]

    for s in strip:
        reg = re.compile(re.escape(s), re.IGNORECASE)
        title = reg.sub(u'', title)
        while title.find(u'  ') >= 0:
            title = title.replace(u'  ', u' ')
        title = title.strip()

    splits = [
        u' - ', u'- ', u' -', # minus
        u' ‒ ', u'‒ ', u' ‒', # U+2012
        u' – ', u'– ', u' –', # U+2013
        u' — ', u'— ', u' —', # U+2014
        u' ― ', u'― ', u' ―', # U+2015
        u' - ', u'- ', u' -', # ?

         u'-', u' ‒', u' –', u' —',
        ]
    split = []
    while len(split) == 0 and len(splits) > 0:
        split = title.split(splits.pop(0))

    if len(split) == 3:
        meta['artist'] = split[1].strip()
        meta['title'] = split[2].strip()
    elif len(split) >= 2:
        meta['artist'] = split[0].strip()
        meta['title'] = split[1].strip()
    else:
        meta['title'] = title

    return meta
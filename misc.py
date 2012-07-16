#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import string
import os
import subprocess

def clean_filename(f):
    special = [u' ', u'.', u',', u'_', u'-', u'=', u'+', u'#', u'¤', 
        u'%', u'&', u'¨', u'^', u'~', u'(', u')', u'[', u']', 
        u'{', u'}', u'!', u'@', u'£', u'$', u'€', u'´', u'`']
    n = u''.join([c for c in f if c.isalpha() or c.isdigit() or c in special])
    n = n.strip()
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
    ]
    for pair in replace:
        n = n.replace(pair[0], pair[1])
    
    n = n.encode('ascii', 'ignore')
    return n
    
def ensure_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)
        
def log(obj):
    sys.stdout.flush()
    if type(obj) == type([]):
        for t in obj:
            sys.stdout.write(t.encode('ascii', 'replace') + '\n')
            sys.stdout.flush()
    elif type(obj) == type('') or type(obj) == type(u''):
        sys.stdout.write(obj.encode('ascii', 'replace') + '\n')
        sys.stdout.flush()
    else:
        try:
            print obj
        except:
            return
    
def clear():
    os.system(['clear','cls'][os.name == 'nt'])
    
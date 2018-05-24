#!/usr/bin/python

import pyperclip
from time import sleep

# pyperclip.copy('Hello world!')

CLIP = pyperclip.paste()

while True :
    sleep( 1 ) # sleep 1 seconf
    clip = pyperclip.paste()
    if clip != CLIP :
        CLIP = clip
        print clip
    
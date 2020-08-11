#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2020 Srevin Saju

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

-----------------------------
This file is part of AppImage Catalog Generator
"""

with open('static/app/app.html', 'r') as r:
    APPTEMPLATE = r.read()

FEED_URL_JSON = "https://appimage.github.io/feed.json"

CATEGORIES = ['Audio', 'Office', 'AudioVideo', 'Science', 'Development',
              'Settings', 'Education', 'System', 'Game', 'Utility',
              'Graphics', 'Video', 'Network']

with open('static/templates/card.html', 'r') as r:
    CARD_TEMPLATE = r.read()

DOWNLOAD_BUTTON_HTML = \
    '<a href="{url}" target="_blank"><button ' \
    'class="button appimage-store-button">' \
    '<span class="icon"><i class="fa fa-download"></i></span>' \
    '<span class="sr-only">Download</span>'\
    '<span>{name}</span>' \
    '<span class="tag is-success" style="margin: 0 0 0 1em">{size}</span>' \
    '<a href="zap://install?app={appname}&tag={tag}&id={uid}" ' \
    'target="_blank"><span class="tag is-warning" ' \
    'style="margin: 0 0 0 1em"><i aria-hidden="true" class="fa ' \
    'fa-bolt"></i><span class="sr-only">Install with Zap</span></span></a>' \
    '</button></a>'

RELEASES_BUTTON_HTML = \
    '<a href="{url}" target="_blank"><button ' \
    'class="button appimage-store-button">' \
    '<span class="icon"><i class="fa fa-upload"></i></span>' \
    '<span>Releases</span>' \
    '</button></a>'

TAG_HTML = \
    '<div class="control">' \
    '<div class="tags has-addons">' \
    '<span class="tag is-dark">{left}</span>' \
    '<span class="tag is-{color}">{right}</span>' \
    '</div></div>'

TAG_CATEGORY_HTML = \
    '<div class="control">' \
    '<div class="tags has-addons">' \
    '<a class="tag is-link" href="{link_to_category}">{category}</a>' \
    '<span class="tag is-dark">#</span>' \
    '</div>' \
    '</div>'

TAGS_GROUP_HTML = \
    '<div class="field is-grouped is-grouped-multiline ' \
    'appimage-tags-group appimage-left-top-margin">{}</div>'

TAGS_GROUP_NO_MARGIN_HTML = \
    '<div class="field is-grouped is-grouped-multiline ' \
    'appimage-tags-group">{}</div>'

GROUPED_BORDER_HTML = \
    '''<div class="appimage-group-light-border">{}</div>'''

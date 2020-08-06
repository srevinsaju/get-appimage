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

CARD_TEMPLATE = \
    '<div class="grid__item"><div class="card appimage-card mb-medium">' \
    '<div class="card-content">' \
    '<div class="media">' \
    '<div class="media-left">' \
    '<figure class="image is-128x128">' \
    '<img src="{image_src}" style="position:absolute; top:0; left:0; ' \
    'width:100%;" alt="{appimage_name} logo" loading="lazy">' \
    '</figure>' \
    '</div>' \
    '<div class="media-content">' \
    '<p class="title is-4">{appimage_name}</p>' \
    '<p class="subtitle is-6">{appimage_maintainer}</p>' \
    '</div>' \
    '</div>' \
    '<div class="content">' \
    '{appimage_summary}' \
    '<br>' \
    '{appimage_categories}' \
    '</div>' \
    '</div>' \
    '<footer class="card-footer appimage-card-footer">' \
    '<a href="https://github.com/{appimage_github}" class="card-footer-item"' \
    'target="_blank rel="noreferrer">' \
    '<i class="fa fa-{is_github} ss-i"></i>' \
    '<span class="ss-card-footer-text">{left_card_description}</span>' \
    '</a>' \
    '<a href="{base_url}/{applink}" class="card-footer-item" target="_blank" '\
    'rel="noreferrer">' \
    '<i class="fa fa-external-link-alt ss-i"></i>' \
    '<span class="ss-card-footer-text">Info</span>' \
    '</a></footer></div></div>'

DOWNLOAD_BUTTON_HTML = \
    '<a href="{url}" target="_blank"><button ' \
    'class="button appimage-store-button">' \
    '<span class="icon"><i class="fa fa-download"></i></span>' \
    '<span>Download {name}</span>' \
    '<span class="tag is-success" style="margin: 0 0 0 1em">{size}</span>' \
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
    '<span class="tag is-info">{right}</span>' \
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
    'appimage-tags-group">{}</div>'



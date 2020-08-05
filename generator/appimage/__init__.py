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

import html
import json
import os
import urllib.request
import uuid

from colorama import Fore

from generator.constants import TAG_HTML, RELEASES_BUTTON_HTML, \
    TAGS_GROUP_HTML, TAG_CATEGORY_HTML, DOWNLOAD_BUTTON_HTML


class AppImage:
    def __init__(self, app, token=None):
        self.token = token
        self._title = html.escape(app.get('name', ''))
        self._categories = app.get('categories')
        self._description = app.get('description')
        self._authors = app.get('authors', [])
        self._licenses = app.get('license')
        self._links = app.get('links')
        self._icon = app.get('icons')
        self._screenshots = app.get('screenshots')
        self.github_info = self.get_github_info()

    @property
    def screenshots_html(self):
        if not self._screenshots:
            return ''
        return '<div><img src="https://gitcdn.xyz/cdn/AppImage/' \
               'appimage.github.io/master/database/{}" ' \
               'class="appimage-screenshot-image"></div>'\
            .format(self._screenshots[0])


    @property
    def maintainer(self):
        return self.authors[0]

    @property
    def categories_html(self):
        categories_tab_html = list()
        for category in self.categories:
            categories_tab_html.append(TAG_CATEGORY_HTML.format(
                category=category,
                link_to_category='../search?q={}'.format(category)
            ))
        return TAGS_GROUP_HTML.format(''.join(categories_tab_html))

    @property
    def is_verified(self):
        if self.github_info:
            if (self._authors[0] == self.github_info.get('author')) or \
                    (self._authors[0] == self.github_info.get('owner')):
                return '<i class="fa fa-shield-alt"></i>'
            else:
                return ''
        else:
            return ''

    @property
    def description(self):
        return self._description

    @property
    def title(self):
        return self._title

    @property
    def title_formatted(self):
        return self._title.replace('_', ' ').replace('-', ' ')


    @property
    def categories(self):
        return self._categories

    @property
    def authors(self):
        if isinstance(self._authors, str):
            return [self._authors]
        elif isinstance(self._authors, list):
            authors = []
            for i in self._authors:
                authors.append(i.get('name'))
            return authors
        else:
            return ['']


    @property
    def licenses(self):
        if isinstance(self._licenses, str):
            return self._licenses,
        else:
            return self._licenses

    @property
    def links(self):
        return self._links

    @property
    def icon(self):
        if isinstance(self._icon, list):
            icon = self._icon[0]
            return 'https://gitcdn.xyz/cdn/AppImage/appimage.github.io/master'\
                   '/database/{}'.format(icon)
        elif isinstance(self._icon, str):
            icon = self._icon
            return 'https://gitcdn.xyz/cdn/AppImage/appimage.github.io/master'\
                   '/database/{}'.format(icon)
        elif self._icon is None:
            icon = '../img/logo.svg'
        else:
            icon = '../img/logo.svg'
        return icon

    @property
    def github(self):
        github_info = self.github_info
        if not github_info:
            return ''

        # buttons
        download_button_html = \
            DOWNLOAD_BUTTON_HTML.format(url=github_info.get("download_url"))

        releases_button_html = \
            RELEASES_BUTTON_HTML.format(url=github_info.get("releases_url"))

        # tags
        latest_tag = \
            TAG_HTML.format(left="Latest",
                            right=github_info.get("latest_release"))

        github_url = \
            TAG_HTML.format(left="<i class='fab fa-github'></i> Github",
                            right=github_info.get("github_url"))

        num_downloads = \
            TAG_HTML.format(left="Downloads",
                            right=github_info.get("download_count"))

        size = \
            TAG_HTML.format(left="Size",
                            right=github_info.get("size"))
        return ''.join((
            TAGS_GROUP_HTML.format(
                '\n'.join((download_button_html, releases_button_html,))),
            TAGS_GROUP_HTML.format(
                '\n'.join((latest_tag, github_url, num_downloads, size)))

        ))

    def get_github_release_from(self, github_release_api):
        request = urllib.request.Request(github_release_api)
        request.add_header("Authorization", "token {}".format(self.token))
        try:
            request_url = urllib.request.urlopen(request)
        except urllib.error.HTTPError:
            print(
                Fore.RED +
                "[STATIC][{}][GH] Request to {} failed with 404".format(
                    self.title, github_release_api
                ) + Fore.RESET)
            return False
        status = request_url.status
        if status != 200:
            print(
                Fore.RED +
                "[STATIC][{}][GH] Request to {} failed with {}".format(
                    self.title, github_release_api, status
                ) + Fore.RESET)
            return False
        return request_url

    def get_github_api_data(self):
        """
        Gets the data from api.github.com
        :return:
        :rtype:
        """
        if not os.path.exists('api'):
            os.makedirs('api')

        # Replace all / to _ for caching
        path_to_local_github_json = \
            os.path.join(
                'api',
                '{}.json'.format(self._links[0].get("url").replace('/', '_'))
            )

        if os.path.exists(path_to_local_github_json):
            with open(path_to_local_github_json, 'r') as r:
                github_api_data = r.read()
            json_data = json.loads(github_api_data)
            if isinstance(json_data, list):
                try:
                    return json_data[0]
                except IndexError:
                    print(json_data)
                    return False
            elif isinstance(json_data, dict):
                return json_data

        github_release_api = \
            "https://api.github.com/repos/{path}/releases/latest".format(
                path=self._links[0].get("url")
            )

        # get the request urllib response instance or bool
        request_url = self.get_github_release_from(github_release_api)
        if not request_url:
            # The request has failed with 404 or some other random error
            # Try again with the superset of releases
            github_release_api = \
                "https://api.github.com/repos/{path}/releases".format(
                    path=self._links[0].get("url")
                )
            request_url = self.get_github_release_from(github_release_api)
            if not request_url:
                # the request still failed :sob:,
                # return that it failed lol
                return request_url

        # read the data
        github_api_data = request_url.read().decode()  # noqa:
        with open(os.path.join('api', "{}.json".format(
                self._links[0].get("url").replace('/', '_'))), 'w') as w:
            w.write(github_api_data)

        # attempt to parse the json data with the hope that the data is json
        try:
            json.loads(github_api_data)
        except json.decoder.JSONDecodeError:
            return False

        # load the data
        json_data = json.loads(github_api_data)
        if isinstance(json_data, list):
            try:
                return json_data[0]
            except IndexError:
                print(json_data)
                return False
        elif isinstance(json_data, dict):
            return json_data

        return False  # nothing has worked :'(

    def get_github_info(self):
        print('[STATIC][{}][GH] Parsing information from GitHub'.format(
            self.title
        ))
        if not self.links:
            return False

        if not len(self._links) >= 1:
            return False

        if not self._links[0].get("type", '').lower() == "github":
            return False

        # process github specific code
        owner = self._links[0].get("url", '').split('/')[0]

        # get api entry-point
        data = self.get_github_api_data()

        if not data:
            # the data we received is ill formatted or can't be processed
            # return False, because at this point, to not raise ValueError
            # and not to stash the build
            return False

        tag_name = data.get("tag_name")

        for i in data.get("assets"):
            download_url = i.get('browser_download_url')
            if download_url.lower().endswith('.appimage'):
                # a valid appimage file found in release assets
                appimage_download_url = download_url
                download_count = i.get('download_count')
                appimage_size = "{0:.2f} MB".format(i.get('size') / (1000 *
                                                                   1000))
                break
        else:
            appimage_download_url = None
            download_count = False
            appimage_size = False

        return {
            'id': uuid.uuid4().hex,
            'owner': owner,
            'author': data.get('author').get('login'),
            'download_url': appimage_download_url,
            'releases_url': "https://github.com/{path}/releases/latest".format(
                path=self._links[0].get("url")
            ),
            'github_url': "https://github.com/{path}".format(
                path=self._links[0].get("url")
            ),
            'download_count': download_count,
            'size': appimage_size,
            'latest_release': tag_name
        }

    def json_data(self):
        return {
            'id': uuid.uuid4().hex,
            'name': self.title,
            'image': self.icon,
            'maintainer': self.maintainer,
            'summary': self.description,
            'github': self.links,
            'categories': self.categories,
            'categories_html': self.categories_html

        }



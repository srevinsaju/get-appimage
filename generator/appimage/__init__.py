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
import hashlib
import html
import json
import os
import urllib.request
import urllib.error
import uuid

import dateutil.parser
from colorama import Fore

from generator.catalog import Catalog
from generator.constants import TAG_HTML, RELEASES_BUTTON_HTML, \
    TAGS_GROUP_HTML, TAG_CATEGORY_HTML, DOWNLOAD_BUTTON_HTML, \
    TAGS_GROUP_NO_MARGIN_HTML, GROUPED_BORDER_HTML


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
        self.catalog = Catalog()

    @property
    def screenshots_html(self):
        if not self._screenshots:
            return ''
        return '<div style="margin: 0 auto; display: block"><img ' \
               'style="margin: 0 auto; ' \
               'display: block;" ' \
               'src="https://gitcdn.xyz/cdn/AppImage/' \
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
        if self.is_github() and self.github_info:
            if (self.maintainer == self.github_info[0].get('author')) or \
                    (self.maintainer == self.github_info[0].get('owner')):
                return True
        return False

    @property
    def is_verified_html(self):
        if self.is_verified:
            return '<i class="fa fa-shield-alt"></i>'
        else:
            return ''

    @property
    def description(self):
        """
        Returns the description of the app

        :return:
        :rtype:
        """
        return self._description

    @property
    def title(self):
        """
        Returns the raw title without formatting, i.e refer title_formatted
        :return:
        :rtype:
        """
        return self._title

    @property
    def title_formatted(self):
        """
        Returns the title but replaces all the _ with ' ' and '-' with ' '
        For un-formatted title (raw title), refer self.title
        :return:
        :rtype:
        """
        return self._title.replace('_', ' ').replace('-', ' ')

    @property
    def categories(self):
        """
        Returns a list of categories
        :return:
        :rtype:
        """
        return self._categories

    @property
    def authors(self):
        """
        Returns a list of authors
        :return:
        :rtype:
        """
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
        """
        Returns the links to the appimage
        :return:
        :rtype:
        """
        return self._links

    @property
    def icon(self):
        """
        Returns icon from feed.json
        :return:
        :rtype:
        """
        if isinstance(self._icon, list):
            icon = self._icon[0]
            return 'https://gitcdn.xyz/cdn/AppImage/appimage.github.io/master'\
                   '/database/{}'.format(icon)
        elif isinstance(self._icon, str):
            icon = self._icon
            return 'https://gitcdn.xyz/cdn/AppImage/appimage.github.io/master'\
                   '/database/{}'.format(icon)
        elif self._icon is None:
            icon = '{}/img/logo.svg'.format(self.catalog.base_url)
        else:
            icon = '{}/img/logo.svg'.format(self.catalog.base_url)
        return icon

    # GitHub api management / data retrieval functions / methods below
    @property
    def github(self):
        """
        Iterates through each release and then generate download button,
        release assets etc. Get the latest continuous / stable / tagged
        releases.
        The iteration continues until any of the following happens
        1. When a *.* tag reaches (inclusive)
        2. When an *untagged* tag is reached (exclusive)
        3. When a [0-9]+ tag is reached (inclusive)
        When the endpoint is reached, the iteration is terminated and then
        the final links are returned as HTML.

        :return: Html string
        :rtype:
        """
        html_data = list()
        if not self.is_github() or not self.github_info:
            # return empty string if its not a github compatible release
            return ''
        for app in self.github_info:
            if not isinstance(app, int):
                continue
            if 'untagged' in self.github_info[app].get('tag'):
                break
            github_links = \
                self.github_generate_buttons_per_release(self.github_info[app])
            html_data.append(github_links)
            if '.' in self.github_info[app].get('tag') or \
                    self.github_info[app].get('tag').isdigit():
                break

        # parse common tags
        if self.github_info.get('source').get('type') == 'github':
            source_code_tag = \
                TAG_HTML.format(
                    left="<i class='fab fa-github margin-right-halfem'></i> "
                         "Github",
                    right=self.github_info.get('source').get('url'),
                    color="info"
                )
            source_code_tag = \
                "<a href='{url}' style='margin-top: 1em; display: block' " \
                "target='_blank'>{tag}</a>".format(
                    url=self.github_info.get('source').get('url'),
                    tag=source_code_tag
                )
        else:
            source_code_tag = ''

        return source_code_tag + ''.join(html_data)

    def github_generate_buttons_per_release(self, github_info):
        # a tag to show URL to github repository

        # shows the latest stable release containing an appimage
        latest_tag = \
            TAG_HTML.format(left="Release",
                            right=github_info.get("tag"),
                            color="success")
        published_at = github_info.get("published_at")
        if published_at:
            published_at = dateutil.parser.parse(published_at)\
                .strftime("%b %d %Y %H:%M:%S")
        else:
            published_at = "Unknown"

        published_on_tag = \
            TAG_HTML.format(left="Published",
                            right=published_at,
                            color="info")

        # a button link to the releases page
        releases_button_html = \
            RELEASES_BUTTON_HTML.format(url=github_info.get("url"))

        # download buttons for all appimages
        download_buttons = list()
        assets = github_info.get('assets')
        for uid in assets:
            download_button_html = \
                DOWNLOAD_BUTTON_HTML.format(
                    url=assets[uid].get("download"),
                    name=assets[uid].get("name"),
                    size=assets[uid].get('size'),
                    appname=self.title_formatted,
                    tag=github_info.get("tag"),
                    uid=uid
                )
            download_buttons.append(download_button_html)

        return GROUPED_BORDER_HTML.format(''.join((
            TAGS_GROUP_HTML.format(
                '\n'.join((latest_tag, published_on_tag))),
            TAGS_GROUP_NO_MARGIN_HTML.format(
                '\n'.join((releases_button_html, ''.join(download_buttons))))
        )))

    def is_github(self):
        """
        Checks if the app-image has its source link from github
        :return:
        :rtype:
        """
        if not self.links:
            return False

        if not len(self._links) >= 1:
            return False

        if not self._links[0].get("type", '').lower() == "github":
            return False

        return True

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
            return json_data

        github_release_api = \
            "https://api.github.com/repos/{path}/releases".format(
                path=self._links[0].get("url")
            )

        # get the request urllib response instance or bool
        request_url = self.get_github_release_from(github_release_api)
        # check if request succeeded:
        if not request_url:
            return False

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
        return json_data

    def get_github_info(self):
        if not self.is_github():
            # pre check if the appimage is from github, if not, exit
            return False

        print('[STATIC][{}][GH] Parsing information from GitHub'.format(
            self.title
        ))

        # process github specific code
        owner = self._links[0].get("url", '').split('/')[0]

        # get api entry-point
        data = self.get_github_api_data()

        if not data or isinstance(data, bool):
            # the data we received is ill formatted or can't be processed
            # return False, because at this point, to not raise ValueError
            # and not to stash the build
            return False

        releases_api_json = dict()
        for i, release in enumerate(data):
            # iterate through the data
            # and process each data
            tag_name = release.get("tag_name")
            appimages_assets = dict()
            for asset in release.get("assets"):
                download_url = asset.get('browser_download_url')
                if download_url.lower().endswith('.appimage'):
                    # a valid appimage file found in release assets
                    appimages_assets[uuid.uuid4().hex] = {
                        'name': asset.get('name'),
                        'download': download_url,
                        'count': asset.get('download_count'),
                        'size': "{0:.2f} MB".format(
                            asset.get('size') / (1000 * 1000))
                    }

            uid_appimage = hashlib.sha256(
                "{}:{}".format(appimages_assets,
                               self._links[0].get("url")).encode()
            ).hexdigest()

            author_json = release.get('author')
            author = None
            if author_json is not None:
                author = author_json.get('login')
            releases_api_json[i] = {
                'id': uid_appimage,
                'author': author,
                'prerelease': release.get('prerelease'),
                'releases': release.get('html_url'),
                'assets': appimages_assets,
                'tag': tag_name,
                'published_at': release.get('published_at')
            }
        releases_api_json['owner'] = owner
        releases_api_json['source'] = {
            'type': 'github',
            'url': "https://github.com/{path}".format(
                    path=self._links[0].get("url"))
        }
        return releases_api_json

    def get_app_metadata(self):
        if self.is_github():
            return self.github_info

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

    def shields_badge(self):
        return {
            "schemaVersion": 1,
            "label": "Get AppImage",
            "message": self.json_data().get('name'),
            "color": "green",
            "logoSvg": "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 16.933 16.933\" height=\"64\" width=\"64\"><g transform=\"matrix(.91146 0 0 .91146 -10.218 1.495)\"><path d=\"M14.558-1.295a1.27 1.27 0 00-1.272 1.272v15.602c0 .704.567 1.27 1.272 1.27H26.7c.704 0 1.271-.566 1.271-1.27V1.892l-3.217-3.187zM19.233.349h2.792V3.14h1.483l-2.88 3.257-2.877-3.257h1.482zM20 7.075h1.32l.049.05c.046.047.053.078.118.513.038.254.073.48.078.502.006.026.032.046.075.06.036.013.141.054.233.093l.166.071.4-.3c.427-.319.45-.33.554-.266.079.048.694.66.814.808.088.11.102.136.102.203 0 .084.011.067-.403.602l-.173.224.055.12c.03.067.077.182.104.257l.05.136.479.075c.263.041.497.08.519.087.088.029.094.07.094.744 0 .662-.006.71-.086.743-.018.005-.252.05-.521.089l-.489.074-.033.091c-.018.05-.063.154-.099.231-.053.116-.062.148-.046.182s.238.321.522.677c.025.03.05.085.056.118.008.052-.002.078-.074.173-.192.257-.736.784-.887.861-.06.03-.081.034-.136.015-.036-.01-.227-.148-.426-.304-.339-.267-.363-.282-.408-.264l-.24.098-.193.078-.021.172c-.028.233-.104.7-.128.783a.222.222 0 01-.066.104c-.045.035-.07.04-.699.04h-.651l-.05-.05c-.046-.049-.053-.077-.118-.512-.037-.254-.073-.48-.078-.502-.006-.025-.032-.049-.075-.06a2.83 2.83 0 01-.234-.094l-.166-.072-.368.28c-.202.154-.387.29-.41.302-.089.049-.15.015-.414-.233a6.032 6.032 0 01-.574-.586c-.09-.108-.103-.132-.103-.202 0-.09.005-.096.367-.56l.21-.27-.068-.147a2.858 2.858 0 01-.1-.249.635.635 0 00-.044-.113 5.501 5.501 0 00-.496-.085 4.552 4.552 0 01-.518-.094c-.07-.044-.076-.089-.076-.734 0-.66.006-.707.086-.742.018-.007.252-.047.52-.088l.486-.074.044-.117c.025-.065.07-.174.101-.241l.057-.123-.066-.095a12.025 12.025 0 00-.293-.382 2.895 2.895 0 01-.238-.327c-.014-.056.012-.114.103-.23a7.76 7.76 0 01.697-.703c.159-.128.224-.158.295-.133.029.01.217.147.42.304.345.267.371.284.415.266l.239-.099.192-.077.032-.245c.036-.281.093-.615.119-.705a.302.302 0 01.057-.105zm.664 2.647c-.74 0-1.323.584-1.323 1.323 0 .53.301.996.787 1.216.23.104.55.136.821.08a1.325 1.325 0 00-.285-2.619z\" fill=\"#efefef\"/><path d=\"M20.367 7.08c-.005.025-.014.047-.014.087V8.23a.224.224 0 01-.175.218c-.297.067-.576.19-.829.349a.224.224 0 01-.276-.03l-.756-.755c-.025-.025-.039-.031-.058-.044l-.567.567c.013.02.019.034.044.058l.756.756a.224.224 0 01.029.277c-.16.252-.282.531-.35.828a.224.224 0 01-.218.175h-1.06c-.042 0-.063.01-.088.015v.814c.025.005.046.014.087.014h1.061a.224.224 0 01.219.175c.067.297.189.576.349.829a.224.224 0 01-.03.276l-.755.756c-.025.024-.031.04-.044.058l.567.567c.02-.014.033-.02.058-.044l.756-.756a.224.224 0 01.276-.03c.253.16.532.282.83.35a.224.224 0 01.174.218v1.06c0 .04.009.063.014.088h.815c.005-.024.014-.049.014-.087V13.87a.224.224 0 01.175-.218c.297-.068.576-.19.828-.35a.224.224 0 01.277.03l.756.756c.025.025.038.03.058.044l.567-.567c-.013-.02-.019-.034-.044-.058l-.756-.756a.224.224 0 01-.029-.276 2.66 2.66 0 00.35-.83.224.224 0 01.217-.174h1.062c.04 0 .062-.01.087-.014v-.814c-.025-.006-.047-.015-.087-.015h-1.062a.224.224 0 01-.218-.175 2.662 2.662 0 00-.35-.828.224.224 0 01.03-.277l.756-.756c.025-.025.03-.038.043-.058l-.567-.567c-.019.013-.033.019-.058.044l-.756.756a.224.224 0 01-.276.029 2.662 2.662 0 00-.829-.35.224.224 0 01-.174-.217V7.167c0-.04-.01-.062-.015-.087zm.407 2.457c.834 0 1.513.679 1.513 1.512 0 .834-.679 1.512-1.513 1.512a1.514 1.514 0 01-1.512-1.512c0-.833.679-1.512 1.512-1.512z\" style=\"marker:none\" overflow=\"visible\" fill=\"none\"/><path d=\"M16.696 10.642v.352c0-.18.005-.257.008-.352zm2.713 0a1.322 1.322 0 00.72 1.618c.23.105.55.137.821.08a1.325 1.325 0 001.01-1.009c.05-.242.028-.475-.04-.689zm5.216 0c.004.108.01.186.01.412 0 .662-.006.71-.086.743-.018.005-.252.05-.521.089l-.489.074-.033.091c-.018.05-.063.154-.099.231-.053.116-.062.148-.046.182s.238.321.522.677c.025.03.05.085.056.118.008.052-.002.078-.074.173-.192.257-.736.784-.887.861-.06.03-.081.034-.136.015-.036-.01-.227-.148-.426-.304-.339-.267-.363-.282-.408-.264l-.24.098-.193.078-.021.172c-.028.233-.104.7-.128.783a.222.222 0 01-.066.104c-.045.035-.07.04-.699.04h-.651l-.05-.05c-.046-.049-.053-.077-.118-.512-.037-.254-.073-.48-.078-.502-.006-.025-.032-.049-.075-.06a2.83 2.83 0 01-.234-.094l-.166-.072-.368.28c-.202.154-.387.29-.41.302-.089.049-.15.015-.414-.233a6.032 6.032 0 01-.574-.586c-.09-.108-.103-.132-.103-.202 0-.09.005-.096.367-.56l.21-.27-.068-.147a2.858 2.858 0 01-.1-.249.635.635 0 00-.044-.113 5.501 5.501 0 00-.496-.085 4.552 4.552 0 01-.518-.094c-.068-.043-.074-.111-.075-.688v5.771h7.947v-6.209z\" fill=\"#e6e6e6\"/><circle r=\"1.632\" cy=\"11.103\" cx=\"20.72\" fill=\"#efefef\"/><path d=\"M24.745-1.295V.73a1.15 1.15 0 001.153 1.152h2.065l-.34-.335L25.085-.96z\" fill=\"#bebebe\"/></g></svg>"
        }

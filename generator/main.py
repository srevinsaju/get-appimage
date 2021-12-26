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

import sys
import os
import time
import urllib.request
import json
from copy import copy

import mistune
from jinja2 import Environment, FileSystemLoader
from colorama import init as colorama_init
from colorama import Fore
from progressbar import progressbar

from generator.appimage.card import Card
from .cli import parse_args, version
from .constants import (
    CARD_TEMPLATE,
    APPTEMPLATE,
    CATEGORIES,
    SITEMAP_URL,
    SITEMAP_HEADER,
    APPTEMPLATE_MD,
)
from .utils import (
    ask_to_remove,
    copytree,
    read_parse_and_write_template,
    get_github_token,
)
from .appimage import AppImage
from .catalog import Catalog

# parse arguments
args = parse_args()


class LibraryBuilder:
    def __init__(
        self,
        output_directory=args.output_directory,
        input_directory=args.input_directory,
    ):
        """
        Handles building the appimage catalog
        :param output_directory:
        :type output_directory:
        """
        self.data = dict()
        self.apps = dict()
        self.json = list()
        self.output_directory = output_directory
        self.file_system_loader = FileSystemLoader(
            os.path.join(input_directory, "static", "templates")
        )

    def write_json_index(self):
        """
        Write JSON index file
        :return:
        :rtype:
        """
        with open(os.path.join(self.output_directory, "index.min.json"), "w") as w:
            json.dump(self.json, w)

    def set_json(self, path):
        """
        sets the self.json to the data from `path`
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, "r") as r:
            self.json = json.load(r)

    def fetch_feed_json(self, force_refresh=False):
        """
        Fetches information from --feed-json and returns the json data
        as python dictionary
        :return:
        :rtype:
        """
        if not os.path.exists(self.output_directory):
            self.create_root_directory(self.output_directory)

        if not force_refresh and os.path.exists(
            os.path.join(self.output_directory, "feed.json")
        ):
            print("[UPSTREAM] Cached feed.json found <=>. ")
            with open(os.path.join(self.output_directory, "feed.json"), "r") as r:
                self.data = json.loads(r.read())
                self.apps = self.data.get("items", dict())
                return

        print("[UPSTREAM] Fetching latest feed.json: {}".format(args.feed_json))
        with urllib.request.urlopen(args.feed_json) as url:
            data = json.loads(url.read().decode())

        get_appimage_feed_json = os.path.join("database", "get_appimage.json")
        if os.path.exists(get_appimage_feed_json):
            with open(get_appimage_feed_json, "r") as fp:
                data2 = json.load(fp)
        else:
            data2 = dict()
        self.data = {**data, **data2}
        self.apps = self.data.get("items", dict())
        with open(os.path.join(self.output_directory, "feed.json"), "w") as w:
            json.dump(data, w)

    @staticmethod
    def create_root_directory(output_directory):
        """
        Creates the output directory if it does not exists. If it exists,
        then prompt the user for confirmation in removing the root output
        directory.
        :param output_directory:
        :type output_directory:
        :return:
        :rtype:
        """
        ask_to_remove(output_directory, noconfirm=args.noconfirm)
        os.makedirs(output_directory)

    def create_static_directories(self, output_directory):
        """
        Creates the 'css', 'img' and 'js' directories, copies the files
        recursively to the destination directory

        Reads the $ROOT/index.html and formats them following specifications
        from the Catalog instance

        :param output_directory:
        :type output_directory:
        :return:
        :rtype:
        """

        for directory in ("css", "img", "js", "search", "badges", "favicon"):
            print("[STATIC] Copying {}".format(directory))
            directory_abspath = os.path.abspath(os.path.join("static", directory))
            output_directory_abspath = os.path.abspath(
                os.path.join(output_directory, directory)
            )

            # create directories
            if not os.path.exists(output_directory_abspath):
                os.makedirs(output_directory_abspath)
            copytree(directory_abspath, output_directory_abspath)

        # Read the index.html jinja2 template and parse them
        # with the values from Catalog Object
        index_html_template_path = os.path.abspath(os.path.join("static", "index.html"))
        index_html_parsed_output_path = os.path.abspath(
            os.path.join(output_directory, "index.html")
        )

        read_parse_and_write_template(
            self.file_system_loader,
            index_html_template_path,
            index_html_parsed_output_path,
            catalog=Catalog(),
            path_prefix=".",
            next_page_link="/p/0",
        )

        # Read the search.html jinja2 template and parse them
        # with the values from Catalog Object
        search_html_template_path = os.path.abspath(
            os.path.join("static", "search", "index.html")
        )
        search_html_parsed_output_path = os.path.abspath(
            os.path.join(output_directory, "search", "index.html")
        )
        read_parse_and_write_template(
            self.file_system_loader,
            search_html_template_path,
            search_html_parsed_output_path,
            catalog=Catalog(),
            path_prefix="..",
        )

    def generate_app_pages(self):
        # create all directories
        self.create_root_directory(self.output_directory)
        appimage_template = Environment(loader=self.file_system_loader).from_string(
            APPTEMPLATE
        )
        appimage_data_template = Environment(
            loader=self.file_system_loader
        ).from_string(mistune.html(APPTEMPLATE_MD))
        sitemap_content = []
        current_formatted_time = time.strftime("%Y-%m-%d")

        # iterate and generate app pages
        for app in progressbar(self.apps, redirect_stdout=True):
            appimage = AppImage(app, token=get_github_token(args))
            path_to_appfolder = os.path.join(
                self.output_directory, appimage.title.lower()
            )

            # make the app folder
            if os.path.exists(path_to_appfolder):
                print(
                    Fore.YELLOW
                    + "[STATIC][{}] Directory exists.".format(appimage.title)
                    + Fore.RESET
                )
            else:
                os.makedirs(path_to_appfolder)

            # write html file
            print(
                Fore.GREEN
                + "[STATIC][{}] Processing HTML files.".format(appimage.title)
                + Fore.RESET
            )

            with open(os.path.join(path_to_appfolder, "index.html"), "w") as w:
                w.write(
                    appimage_template.render(
                        appimage=appimage,
                        catalog=Catalog(),
                        content=appimage_data_template.render(appimage=appimage),
                    )
                )
            _app_sitemap_local = SITEMAP_URL.format(
                url=f"{Catalog().url}/{appimage.title_formatted}",
                lastmod=current_formatted_time,
                changefreq="weekly",
            )
            sitemap_content.append(_app_sitemap_local)

            self.json.append(appimage.json_data())
            with open(os.path.join(path_to_appfolder, "core.json"), "w") as w:
                json.dump(appimage.get_app_metadata(), w)
            shields_badge = appimage.shields_badge()
            with open(os.path.join(path_to_appfolder, "shields.json"), "w") as w:
                json.dump(shields_badge, w)

        # write json file
        self.write_json_index()

        with open(os.path.join(self.output_directory, "sitemap.xml"), "w") as w:
            w.write(SITEMAP_HEADER.format(content="".join(sitemap_content)))
        print("writing sitemap.xml completed successfully")

    def generate_categories_pages(self):
        print("Generating Categories list")
        categories_list_directory_path = os.path.join(
            self.output_directory, "categories"
        )

        print("[STATIC] Reading index.html template")
        index_html_path = os.path.abspath(os.path.join("static", "all", "index.html"))
        with open(index_html_path, "r") as index_html_buffer:
            index_html_template = Environment(
                loader=self.file_system_loader
            ).from_string(index_html_buffer.read())

        # filter apps by category
        apps_by_category = dict(((x, []) for x in CATEGORIES))
        for app in self.json:
            # https://specifications.freedesktop.org/menu-spec/latest/apa.html
            for category in app["categories"]:
                if category not in CATEGORIES:
                    # this category is not a valid desktop file category
                    # as per freedesktop specifications
                    print(
                        Fore.YELLOW + "[STATIC][CATEGORY][W] {} is not a valid desktop "
                        "category ({})".format(category, app["name"]),
                        Fore.RESET,
                    )
                    continue

                apps_by_category[category].append(app)

        for category in CATEGORIES:
            # get the path to the categories
            category_directory_path = os.path.join(
                categories_list_directory_path, category.lower()
            )
            if not os.path.exists(category_directory_path):
                os.makedirs(category_directory_path)

            # create the pages directory
            pages_directory_path = os.path.join(category_directory_path, "p")
            if os.path.exists(pages_directory_path):
                ask_to_remove(pages_directory_path)
            os.makedirs(pages_directory_path)

            self._create_p_directories(
                json_file=apps_by_category[category],
                pages_directory_path=pages_directory_path,
                index_html_template=index_html_template,
            )

            index_html_template_path = os.path.abspath(
                os.path.join("static", "all", "index.html")
            )
            index_html_parsed_output_path = os.path.abspath(
                os.path.join(category_directory_path, "index.html")
            )

            read_parse_and_write_template(
                self.file_system_loader,
                index_html_template_path,
                index_html_parsed_output_path,
                catalog=Catalog(),
                path_prefix="../..",
                next_page_link="/categories/{}/p/0".format(category.lower()),
            )

        index_html_template_path = os.path.abspath(
            os.path.join("static", "categories", "index.html")
        )
        index_html_parsed_output_path = os.path.abspath(
            os.path.join(categories_list_directory_path, "index.html")
        )

        read_parse_and_write_template(
            self.file_system_loader,
            index_html_template_path,
            index_html_parsed_output_path,
            catalog=Catalog(),
            path_prefix="..",
            next_page_link="/p/0",
        )

    def generate_app_list(self):
        """
        Generate app list directories in ./all/ directory
        They are distributed directories in the all directory which containes
        ./all/p/*/index.html with cards corresponding to apps.
        :return:
        :rtype:
        """
        print("Generating App List")
        all_app_list_directory_path = os.path.join(self.output_directory, "all")
        pages_directory_path = os.path.join(all_app_list_directory_path, "p")
        if not os.path.exists(pages_directory_path):
            os.makedirs(pages_directory_path)

        print("[STATIC] Reading index.html template")
        index_html_path = os.path.abspath(os.path.join("static", "all", "index.html"))
        with open(index_html_path, "r") as index_html_buffer:
            index_html_template = Environment(
                loader=self.file_system_loader
            ).from_string(index_html_buffer.read())

        # sort json
        sorted_json = copy(self.json)
        sorted_json.sort(key=lambda x: x["name"].lower())

        # parse
        self._create_p_directories(
            json_file=sorted_json,
            pages_directory_path=pages_directory_path,
            index_html_template=index_html_template,
        )

        index_html_template_path = os.path.abspath(
            os.path.join("static", "all", "index.html")
        )
        index_html_parsed_output_path = os.path.abspath(
            os.path.join(all_app_list_directory_path, "index.html")
        )

        read_parse_and_write_template(
            self.file_system_loader,
            index_html_template_path,
            index_html_parsed_output_path,
            catalog=Catalog(),
            path_prefix="..",
            next_page_link="/all/p/0",
        )

    def _create_p_directories(
        self, json_file, pages_directory_path, index_html_template
    ):
        """
        Internal helper function to create ./p/* directories and files in them
        :param json_file:
        :type json_file:
        :param pages_directory_path:
        :type pages_directory_path:
        :param index_html_template:
        :type index_html_template:
        :return:
        :rtype:
        """
        last_page = True

        # initialize the templates
        card_template = Environment(loader=self.file_system_loader).from_string(
            CARD_TEMPLATE
        )

        for i in range(0, len(json_file), 18)[::-1]:

            directory = os.path.join(pages_directory_path, str(i // 18))
            ask_to_remove(directory, noconfirm=args.noconfirm)
            os.makedirs(directory)

            print("[STATIC] Writing {}".format(directory))
            index_html = os.path.abspath(os.path.join(directory, "index.html"))

            column_data = []
            catalog = Catalog()
            for j, app in enumerate(json_file[i : i + 18]):
                column_data.append(
                    card_template.render(card=Card(app), catalog=catalog)
                )

            next_page_link = "/p/{}".format(i // 18 + 1)
            if last_page:
                last_page = False
                next_page_link = None

            with open(index_html, "w") as w:
                w.write(
                    index_html_template.render(
                        catalog=Catalog(),
                        cards="\n".join(column_data),
                        path_prefix="./../../..",
                        next_page_link=next_page_link,
                    )
                )


def main():
    colorama_init()  # initialize terminal colors for TERM with no colors

    if args.version:
        version()
        sys.exit()

    # initialize the library builder
    lb = LibraryBuilder()

    # refresh the information from feed.json
    lb.fetch_feed_json(force_refresh=args.force_refresh_feed)

    if args.set_json:
        lb.set_json(args.set_json)

    if args.generate_app_pages:
        lb.generate_app_pages()

    if args.copy_theme:
        lb.create_static_directories(lb.output_directory)

    if args.generate_app_list:
        lb.generate_app_list()

    if args.generate_categories_pages:
        lb.generate_categories_pages()


if __name__ == "__main__":
    main()

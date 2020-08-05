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

import argparse
import os

from colorama import Fore

from generator.constants import FEED_URL_JSON

from . import __version__


def parse_args():
    """
    Parses arguments using argparse and returns parse_args()
    :return:
    :rtype:
    """
    parser = argparse.ArgumentParser(
        'AppImage Catalog Generator',
        description='Generates static HTML files for the Appimage catalog'
    )
    parser.add_argument(
        '-i', '--input-directory',
        default=os.getcwd(),
        help='Provide the directory where `static` resides '
             'HTML, (defaults to: {}) '.format(os.getcwd())
    )
    parser.add_argument(
        '-o', '--output-directory',
        default=os.path.join(os.getcwd(), 'catalog-compiled'),
        help='Provide the directory to output the parsed website for Appimage '
             'catalog'
    )
    parser.add_argument(
        '-t', '--copy-theme',
        action='store_true',
        help='Copy the files from static directory to output directory'
    )
    parser.add_argument(
        '-j', '--set-json',
        default='',
        help='Sets an alternative json instead of parsed one '
    )
    parser.add_argument(
        '-g', '--generate-app-pages',
        action='store_true',
        help='Start the process of HTML generation. '
    )
    parser.add_argument(
        '-C', '--force-refresh-feed',
        default='',
        help='Fetches feed.json again, and then parses content rather than '
             'cached copy'
    )
    parser.add_argument(
        '-x', '--generate-sitemap',
        default='',
        help='Generate a sitemap.xml file to the output directory'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='More verbose logging'
    )
    parser.add_argument(
        '-p', '--pull-static-css-js-html',
        default='',
        help="Provide the path to js, css and index.html (default: ./static)"
    )
    parser.add_argument(
        '-O', '--gh-token',
        default='',
        help="Provide the GitHub OAuth token (defaults to: env GH_TOKEN)"
    )
    parser.add_argument(
        '-G', '--generate-app-list',
        action='store_true',
        help="Parses app list"
    )
    parser.add_argument(
        '-P', '--disable-progress-bar',
        action='store_true',
        help="Provides a unique icon name based on bundle id"
    )
    parser.add_argument(
        '-s', '--include-screenshots',
        action='store_true',
        help="Includes screenshots of activity if its found as"
             " <activity>/screenshots/*.png"
    )
    parser.add_argument(
        '-y', '--noconfirm',
        action='store_true',
        help="Replace output directory (default: always ask)"
    )
    parser.add_argument(
        '-c', '--no-colors',
        action='store_true',
        help="Suppress colors in terminal (default: env ANSI_COLORS_DISABLED)"
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help="Show the version"
    )
    args = parser.parse_args()
    return args


def version():
    """
    Shows the version
    :return:
    :rtype:
    """
    print(Fore.GREEN + "AppImageCatalog-2 Generator Tool" + Fore.RESET)
    print(__version__)
    print()


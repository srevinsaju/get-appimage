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

import os
import shutil
import sys
from getpass import getpass

from jinja2 import Environment
from progressbar import progressbar


def read_parse_and_write_template(
        file_system_loader, html_template_path, html_output_path, **kwargs):
    """
    Read HTML Template, parse the HTML template with jinja template
    renderer and write the formatted jinja template to html_output_path with
    kwargs as the argument
    :param file_system_loader: jinja2 FileSystemLoader
    :type file_system_loader: jinja2.FileSystemLoader
    :param html_template_path: Path to the HTML template
    :type html_template_path: str
    :param html_output_path: Path to write the parsed HTML template
    :type html_output_path: str
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """
    output_path_file_name = html_output_path.split(os.path.sep)[-1]

    print("[STATIC] Reading template: {}".format(output_path_file_name))
    with open(html_template_path, 'r') as _buffer:
        html_template = Environment(loader=file_system_loader) \
            .from_string(_buffer.read())

    print("[STATIC] Writing parsed template: {}".format(output_path_file_name))
    with open(html_output_path, 'w') as w:
        w.write(html_template.render(**kwargs))


def ask_to_remove(directory, noconfirm=False):
    """
    Asks the user if they want to remove a directory
    :param noconfirm:
    :type noconfirm:
    :param directory: path to directory
    :type directory:
    :return:
    :rtype:
    """
    if os.path.exists(directory):
        if not noconfirm:
            # ask user for confirmation before removing directory
            proceed = input("The operation will remove {}. "
                            "Are you sure you want to proceed? "
                            "(Y/n) ".format(directory))
            if proceed not in ('y', 'Y'):
                print("Terminated on user request.")
                sys.exit(-1)
        shutil.rmtree(directory, ignore_errors=True)


def copytree(src, dst, symlinks=False, ignore=None):
    """
    Recursively copies directories and files and follow
    symlinks if necessary
    :param src: Path like object (source)
    :type src: str
    :param dst: Path like object (destination)
    :type dst: str
    :param symlinks: Should symlinks be copied?
    :type symlinks: bool
    :param ignore: Ignore all errors?
    :type ignore: bool
    :return: None
    :rtype: None
    """
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            try:
                shutil.copytree(s, d, symlinks, ignore)
            except FileExistsError:
                shutil.rmtree(d)
                shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def check_progressbar(*arg, **kwarg):
    """
    Conditionally show progress bar, return range if progress bar is not
    requested
    :param arg:
    :type arg:
    :param kwarg:
    :type kwarg:
    :return:
    :rtype:
    """
    if kwarg.pop("enable_progressbar"):
        return progressbar(*arg, **kwarg)
    else:
        return list(*arg)


def get_github_token(args):
    """
    Gets the github token
    :return:
    :rtype:
    """
    if os.getenv('GH_TOKEN'):
        return os.getenv('GHTOKEN')
    elif args.gh_token:
        return args.gh_token
    else:
        return None


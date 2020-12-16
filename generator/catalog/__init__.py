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


class Catalog:
    def __init__(self):
        self.title = "Get AppImageX"
        self.description = "Collection of maintained AppImagesX in one website"
        self.author = "Srevin Saju"
        self.root_url = "https://appimage.org"
        self.url = "https://srevinsaju.me/get-appimagex"
        self.image = "/img/logo.svg"
        self.issue_tracker = \
            "https://github.com/srevinsaju/get-appimagex/issues"
        self._keywords = ["AppImage", "Linux", "Package"]
        self.base_url = "/get-appimagex"


    @property
    def keywords(self):
        return ", ".join(self._keywords)

    @property
    def name(self):
        return self.title

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import re

from autopkglib import Processor, ProcessorError

try:
    #import for Python 3
    from six.moves.urllib.request import urlopen 
    from six.moves.html.parser import HTMLParser 
except ImportError:
    #import for Python 2
    from urllib2 import urlopen  
    from HTMLParser import HTMLParser


BASE_URL = "https://www.audiotranskription.de"
REGEX = r"href=\"(/audot/downloadfile\.php\?k=1&amp;d=48&amp;l=de&amp;c=j5i99kpxz1)\">Download für Mac \(f5\)"

__all__ = ["F5transkriptURLProvider"]


class F5transkriptURLProvider(Processor):
    """Provides a download URL for the latest version of F5transkript"""

    description = __doc__
    input_variables = {}
    output_variables = {"url": {"description": "URL to latest version"}}

    def main(self):

        try:
            response = urlopen(BASE_URL + "/downloads.html")
            html_source = response.read()
            escaped_url = re.search(REGEX, html_source).group(1)
            url = HTMLParser().unescape(escaped_url)
            if self.env["verbose"] > 0:
                print(
                    "F5transkriptURLProvider: Match found is: %s\n"
                    "F5transkriptURLProvider: Unescaped url is: %s\n"
                    "F5transkriptURLProvider: Returning full url: %s%s"
                    % (escaped_url, url, BASE_URL, url)
                )
        except Exception as err:
            raise ProcessorError("Failed to get download URL: %s" % err)
        self.env["url"] = BASE_URL + url


if __name__ == "__main__":
    processor = F5transkriptURLProvider()
    processor.execute_shell()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Transmission class
#

__author__ = "Jaume Mila"
__version__ = "1.0.1"
__status__ = "Stable"
__file__ = "Request.py"

import urllib
import urllib2
import cookielib


class Requester:
    """
    Transmission class.
    Used statically to open and read pages.
    Used as instance to login and bid managing cookies.
    :param host: string
    :param agent: string
    """

    def __init__(self, host, agent=None):
        self._opener = None  # OpenerDirector
        self._cookie_jar = None  # CookieJar
        self._headers = self.request_headers(host=host, agent=agent)
        self._set_cookiejar()
        pass

    def check_session(self):
        """
        Get "sessionId" cookie value.
        Used to check if user has logged in successfully.
        :return: string
        """
        try:
            for cookie in self._cookie_jar:
                if cookie.name == "vv_sessionId":
                    return cookie.value
        except TypeError:
            raise
        return False

    @property
    def opener(self):
        return self._opener

    @classmethod
    def request_headers(cls, host, agent):
        """
        Returns request headers based on different modes
        :param host: string
        :param agent: string
        :return list<tuple>
        """
        referer = "https://www.google.com"

        headers = [
            ("Host", host),
            ("User-Agent", agent),
            ("Accept", "application/json, text/plain, */*"),
            ("Accept-Language", "en-US,en;q=0.5"),
            ("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8"),
            ("Connection", "keep-alive"),
            ("Pragma", "no-cache"),
            ("Cache-Control", "no-cache"),
            ("Referer", referer)]

        return headers

    def _set_cookiejar(self):
        """
        Initializes _cookie_jar and _opener for a persistent session.
        """
        self._cookie_jar = cookielib.CookieJar()
        self._opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self._cookie_jar))
        self._opener.addheaders = self._headers

    @classmethod
    def open_request(cls, request, post_fields=None, opener=None, timeout=None):
        """
        Opens request and returns response.
        If parameter opener is not empty opens by urlopen else opens by opener.
        HTTP request will be a POST instead of a GET when the data parameter is
        provided.
        :param request: string url
        :param post_fields: dict post data fields, if it's none the used method
        :param timeout: int
        will be get.
        :exception HTTPError
        :exception URLError
        :exception Exception
        :return HTTP Response
        """
        if not post_fields is None:
            data = urllib.urlencode(post_fields)
        else:
            data = post_fields

        try:
            if opener is None:
                response = urllib2.urlopen(request, data)
            else:
                response = opener.open(request, data, timeout)

        except urllib2.HTTPError:
            raise

        except urllib2.URLError:
            raise

        except Exception:
            raise

        return response

    @classmethod
    def read_response(cls, response):
        """
        Gets page content by url
        :param response: HTTP Response
        :return: string
        """
        try:
            content = response.read()

        except Exception:
            raise

        return content

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value
        pass

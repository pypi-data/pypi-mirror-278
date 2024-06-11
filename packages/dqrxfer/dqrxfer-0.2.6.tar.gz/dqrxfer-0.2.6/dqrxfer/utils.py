#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2022 Joseph Areeda <joseph.areeda@ligo.org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""""""

import http.cookiejar
import os
from pathlib import Path

import ciecplib
from lxml.etree import XMLSyntaxError


def get_shib_cookie_jar(url, idp=None, kerberos=True, username=None):
    """
    Log in wih shibboleth if needed and return needed cookies
    :param str url: server url
    :param str idp: override default IdP
    :param kerberos: use Kerberos for authentication
    :return: A cookie jar needed to access shib protected site
    """
    cjar = http.cookiejar.CookieJar()
    try:
        user = os.getenv('USER') if username is None else username
        print(f'Using {user} for ecp cookie')
        cookie = ciecplib.get_cookie(url, kerberos=kerberos, username=user)
        cjar.set_cookie(cookie)
    except XMLSyntaxError:
        pass
    return cjar


def get(url, cookiejar=None, kerberos=True):
    """
    Use http get to access shib protected URI
    :param str url: site address with get arguments
    :param http.cookiejar.CookieJar cookiejar: Session cookie if needed`
    :param bool kerberos:
    :return requests.Response:
    """
    r = ciecplib.get(url, kerberos=kerberos, cookiejar=cookiejar)
    return r


def file_upload(url, cookiejar, files, params):
    """
    upload files and other parameter
    :param str url: where to upload eg: https://dqr.ligo.caltech.edu/dqr/Upload
    :param CookieJar cookiejar: necessary coodies for Shibboleth
    :param list files: paths to files to upload
    :param dict params: not file form fields
    :return: None
    """
    filelist = list()
    for k, v in params.items():
        filelist.append((k, v))

    for file in files:
        p = Path(file)
        filelist.append((p.name, p.open('rb')))

    res = ciecplib.post(url=url, cookiejar=cookiejar, files=filelist)
    return res.status_code, res.content, res.headers['Content-Type']

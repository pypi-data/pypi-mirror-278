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
import os
import time

start_time = time.time()

import argparse
from dqrxfer import utils
import logging

from dqrxfer._version import __version__

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'dqr-xfer'


def main():
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    ktname = os.getenv('KRB5_KTNAME')
    user = os.getenv('USER') if ktname is None else ktname

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('--server', default='https://dqr.ligo.caltech.edu', help='Address of dqr web server')
    parser.add_argument('--user', default=user, help='User/principal of kerberos used to login')

    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    url = args.server + '/dqr/Ping'
    user = args.user
    start = time.time()
    cjar = utils.get_shib_cookie_jar(url, username=user)
    cookie_time = time.time() - start

    nping = 0
    nsucceed = 0
    ptimes = list()
    for i in range(3):
        start = time.time()
        nping += 1
        r = utils.get(url, cjar)
        get_time = time.time() - start
        our_unix_time = int(time.time_ns() * 1e-6)
        if r.status_code == 200:
            print('OK')
            nsucceed += 1
            their_unix_time = int(r.content.decode('utf-8').strip())
            tdif = (our_unix_time - their_unix_time) / 1000.
            ptimes.append(tdif)
            logger.debug(f'Time difference {tdif:.3f}s')
        else:
            print(f'fail. Code: {r.status_code}')
        logger.info(f'Login: {cookie_time:.2f}, Ping: {get_time:.2f}, status:{r.status_code}')
    logger.info(f'Success = {nsucceed * 100 / nping}%')
    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    main()

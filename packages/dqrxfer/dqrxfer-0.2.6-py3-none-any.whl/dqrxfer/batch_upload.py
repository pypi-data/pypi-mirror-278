#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: nu:ai:ts=4:sw=4

#
#  Copyright (C) 2023 Joseph Areeda <joseph.areeda@ligo.org>
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

import time

start_time = time.time()

import argparse
import logging
from pathlib import Path
import re
import subprocess

__author__ = 'joseph areeda'
__email__ = 'joseph.areeda@ligo.org'
__process_name__ = 'dqrxfer'
from dqrxfer._version import __version__


def main():
    logging.basicConfig()
    logger = logging.getLogger(__process_name__)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-d', '--indir', type=Path, help='DQR result directory to search')
    parser.add_argument('-p', '--project', help='Project for database entry')
    parser.add_argument('-u', '--uploader', help='ID of site producing this report. eg: LLO, LHO, Kagra, EGO')
    parser.add_argument('--set-dir', action='store_true', help='Tis is at CIT')
    parser.add_argument('-s', '--server', default='dqr.ligo.caltech.edu', help='Remote DQR server')
    parser.add_argument('--test', action='store_true', help='print command but do not upload')

    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    indir = Path(args.indir)
    uploader = str(args.uploader)
    project = args.project

    # debugging?
    logger.debug(f'{__process_name__} version: {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    flist = list(indir.glob('*_dir/*'))

    for file in flist:
        fproc_start = time.time()
        if not file.is_dir():
            continue
        name = file.name

        filpat = '([^_]+)_(\\d+)'
        m = re.match(filpat, name)

        if m is None:
            filpat = '([^_]+)_([^_]+)_(\\d+)'
            m = re.match(filpat, name)

        if m:
            graceid = m.group(1)
            if len(m.groups()) == 2:
                site = uploader
                version = int(m.group(2))
            else:
                site = m.group(2)
                version = m.group(3)

            if site.lower() == 'cit':
                prog = 'dqr-upload'
                cmd = [prog, '-vv', '--graceid', graceid, '--uploader', site,
                       '--project', project, '--revision', f'{version}', '--set-dir', str(file.absolute())]
            else:
                prog = '/home/dqr/src/dqr-configuration-files/O4/online/L1/bin/tar_and_upload.sh'
                cmd = [prog, graceid, str(file.absolute()), f'{version}']

            cmd_str = " ".join(cmd)
            logger.info(f'upload command:\n    {cmd_str}')
        else:
            logger.debug(f'Directory rejected: {str(file.name)}')
            continue

        if args.test:
            continue

        r = subprocess.run(cmd, capture_output=True)
        upload_time = time.time() - fproc_start
        if r.returncode == 0:
            logger.info(f'file upload succeeded in {upload_time:,.1f} seconds, ')
        else:
            logger.critical(f'file upload returned an error: {r.returncode}. STDERR:\n {r.stderr.decode("utf-8")}')

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    main()

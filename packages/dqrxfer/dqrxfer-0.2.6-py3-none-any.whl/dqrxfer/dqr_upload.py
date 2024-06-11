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

"""
Upload files and directories needed for the Data Quality Reports to the central report facility.
"""
import json
import os
import subprocess
import time

from dqrxfer import utils

start_time = time.time()

import argparse
import logging
from pathlib import Path
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
    tempdir = Path(os.getenv('TMPDIR', '/tmp'))

    parser = argparse.ArgumentParser(description=__doc__, prog=__process_name__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', action='count', default=1,
                        help='increase verbose output')
    parser.add_argument('-V', '--version', action='version',
                        version=__version__)
    parser.add_argument('-q', '--quiet', default=False, action='store_true',
                        help='show only fatal errors')
    parser.add_argument('-s', '--server', default='dqr.ligo.caltech.edu', help='Remote DQR server')
    parser.add_argument('--port', default=22, help='Port for ssh/scp')
    parser.add_argument('--retries', default=3, help='We can retry failure in scp and ssh command')
    parser.add_argument('--retry-wait', type=int, default=60, help='Time in seconds to wait between retries')
    parser.add_argument('-g', '--graceid', help='Event ID')
    parser.add_argument('-u', '--uploader', help='ID of site producing this report. eg: LLO, LHO, Kagra, EGO')
    parser.add_argument('-p', '--project', help='Project that the analysis belongs to. '
                                                'eg: replay, mdc, o4, personal')
    parser.add_argument('--user', default=user, help='User/principal of kerberos used to login')
    parser.add_argument('--revision', default='1', help='Which dqr run (version of the report)')
    parser.add_argument('--subdir', help='Send these files to a subdirectory of report')
    parser.add_argument('--config', default='default', help='Our config file')
    parser.add_argument('--set-dir', type=Path, help='Specify a directory path at home (CIT) to make a '
                                                     'database entry without transferring any files.')
    parser.add_argument('--use-https', action='store_true', help='use web transfer rather thanscp/ssh')
    parser.add_argument('--upload-path', default='/home/dqr/xfer', help='For scp transfers where to put files')
    parser.add_argument('--remote-command', default='/usr/local/dqr/bin/dqr_proces_upload.sh',
                        help='Command to run on upload server after files have been transferred')
    parser.add_argument('--temp-dir', type=Path, default=tempdir,
                        help='Temporary directory to use for intermediate files')
    parser.add_argument('files', nargs='*', type=Path, help='File or directory to upload')

    args = parser.parse_args()
    verbosity = 0 if args.quiet else args.verbose

    if verbosity < 1:
        logger.setLevel(logging.CRITICAL)
    elif verbosity < 2:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)

    # debugging?
    logger.debug(f'{__process_name__} version {__version__} called with arguments:')
    for k, v in args.__dict__.items():
        logger.debug('    {} = {}'.format(k, v))

    # upload files
    params = {'event': args.graceid, 'uploader': args.uploader, 'revision': args.revision, 'config': args.config,
              'project': args.project, 'subdir': args.subdir, 'set_dir': str(args.set_dir)}

    user = args.user
    temp_path = Path(args.temp_dir)
    temp_path.mkdir(0o755, parents=True, exist_ok=True)

    if args.use_https:
        url = f"https://{args.server}/dqr/Upload"

        # Shibboleth log in
        start = time.time()
        cjar = utils.get_shib_cookie_jar(url, username=user)
        cookie_time = time.time() - start

        start = time.time()
        status, content, content_type = utils.file_upload(url, cjar, args.files, params)
        upload_time = time.time() - start
        response_stats = json.loads(content.decode('utf-8'))
        tot_size = 0
        rstat = response_stats['status']
        stat = 'Success' if status == 200 and rstat == 0 else 'Fail'

        if rstat == 0:

            for fname, fsize in response_stats['files'].items():
                tot_size += fsize
            upload_rate = tot_size / 1000. / upload_time
            logger.info(f'Upload: {stat} authentication {cookie_time:.2f}s, '
                        f'xfer: {tot_size/1000.:.0f}KB {upload_time:.2f}s {upload_rate:.0f}KBps')
        else:
            logger.error(f'https - upload failed. It returned {rstat}')
        logger.debug(f'content:\n{content.decode("utf-8")}')
        logger.info(f'Status: {stat}, content_type: {content_type}')
    else:
        # Use scp/ssh for transfer
        upload_path = Path(args.upload_path)
        scp_destination = f"{args.server}:{upload_path}/"
        start = time.time()
        json_file_name = f'{params["event"]}-{params["revision"]}-{params["project"]}-{params["uploader"]}-upload.json'
        json_file = temp_path / json_file_name
        with json_file.open('w') as jfp:
            json.dump(params, jfp, indent=4)
        bytes_sent = json_file.stat().st_size
        scp_cmd = ['scp', '-P', str(args.port), str(json_file.absolute())]

        for f in args.files:
            if f.exists():
                bytes_sent += f.stat().st_size
                scp_cmd.append(str(f.absolute()))
        scp_cmd.append(scp_destination)
        logger.debug(f'scp command:\n   {" ".join(scp_cmd)}')

        retries = args.retries
        returncode = -1
        while retries > 0:
            r = subprocess.run(scp_cmd, capture_output=True)
            upload_time = time.time() - start
            returncode = r.returncode
            if returncode == 0:
                logger.info(f'scp succeeded in {upload_time:,.1f} seconds, '
                            f'{bytes_sent:,} bytes, {bytes_sent/upload_time/1000.:,.1f} KB/s')
                break
            else:
                logger.critical(f'scp returned an error: {r.returncode}. STDERR:\n {r.stderr.decode("utf-8")}')
                if args.retry_wait > 0 and retries > 1:
                    logger.info(f'Waiting {args.retry_wait} seconds before retry')
                    time.sleep(args.retry_wait)

            retries -= 1
        if returncode != 0:
            logger.critical(f'The {args.retries} have been exhaused. Last error {returncode}')
            exit(3)

        # start the process to incorporate upload
        remote_process_start = time.time()
        remote_json = upload_path / json_file.name
        remote_files = list()
        for f in args.files:
            rf = upload_path / f.name
            remote_files.append(str(rf.absolute()))

        proc_upload_cmd = ["ssh", args.server, '-p', str(args.port), args.remote_command, '--json',
                           str(remote_json.absolute())]
        proc_upload_cmd.extend(remote_files)
        logger.debug(f'Remote process command:\n   {" ".join(proc_upload_cmd)}')
        retries = args.retries
        while retries > 0:
            r = subprocess.run(proc_upload_cmd, capture_output=True)
            remote_process_time = time.time() - remote_process_start
            returncode = r.returncode
            if returncode == 0:
                logger.info(f'Remote process upload succeeded in {remote_process_time:,.1f} seconds, ')
                break
            else:
                logger.critical(f'Remote process upload returned an error: {r.returncode}. '
                                f'STDERR:\n {r.stderr.decode("utf-8")}')
                if args.retry_wait > 0 and retries > 1:
                    logger.info(f'Waiting {args.retry_wait} seconds before retry')
                    time.sleep(args.retry_wait)

            retries -= 1
        if returncode != 0:
            logger.critical(f'The {args.retries} have been exhausted. The last returncode was {returncode}')
            exit(3)

    # report our run time
    logger.info(f'Elapsed time: {time.time() - start_time:.1f}s')


if __name__ == "__main__":
    main()

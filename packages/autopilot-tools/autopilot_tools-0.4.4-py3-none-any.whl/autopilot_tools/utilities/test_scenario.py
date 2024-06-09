#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>
import argparse
import logging
import os
import sys
from time import time
from autopilot_tools.vehicle import Vehicle
from autopilot_tools.mission_file.mission_result import StatusCode
from autopilot_tools.mavlink_ftp.ftp_filesystem import File
from autopilot_tools.enums import Devices
from autopilot_tools.enums import AutopilotTypes

logger = logging.getLogger(__name__)

def run_scenario():
    parser = argparse.ArgumentParser(
        prog='Run the test scenario',
        description='This utility uploads mission to HITL/SITL simulator, '
                    'waits for completion, then collects and processes the '
                    'resulting log with https://logs.px4.io/')

    parser.add_argument(
        'mission', help='mission file in .plan format', type=str)
    parser.add_argument(
        '-p', '--device', dest='device', choices=list(Devices), type=str, default='udp',
        help='either udp (SITL) or serial (HITL)')
    parser.add_argument(
        '-t', '--timeout', dest='timeout', type=int, default=200,
        help='run mission for this long')
    parser.add_argument(
        '-o', '--output', dest='output', default=None, type=str,
        help='directory where to store downloaded log')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.add_argument('-vv', '--super-verbose', dest='super_verbose', action='store_true')
    args = parser.parse_args()
    if args.super_verbose:
        logger.setLevel(logging.DEBUG)
    elif args.verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.CRITICAL)

    v = Vehicle()
    v.connect(device=args.device)
    result = v.load_mission(args.mission)

    if result != StatusCode.OK:
        logger.critical(f'Mission upload failed with code {result}')
        sys.exit(1)
    result = v.run_mission(timeout=args.timeout)
    if result.status == StatusCode.MISSION_TIMEOUT:
        logger.warning('Mission execution timed out. Collecting log for investigation')
    elif result.status != StatusCode.OK:
        logger.critical(f'Mission execution failed: {result}')
        sys.exit(1)
    else:
        logger.info('Mission executed successfully')

    logger.info('Downloading log')
    latest_file: File = v.mav_ftp.get_last_log(v.get_log_folder())
    start_time = time()
    latest_file.materialize()
    logger.info(f'Downloaded {latest_file.size}B in {time() - start_time:.2f} s')

    if args.output is not None:
        latest_file.save_locally(args.output)
        logger.info(f"Saved log file to {os.path.abspath(args.output)}")

    if v.autopilot == AutopilotTypes.PX4:
        logger.info('Uploading to https://logs.px4.io')
        result.log_link = v.analyze_log(latest_file.data)
    logger.ok_cyan(result)


if __name__ == '__main__':
    run_scenario()

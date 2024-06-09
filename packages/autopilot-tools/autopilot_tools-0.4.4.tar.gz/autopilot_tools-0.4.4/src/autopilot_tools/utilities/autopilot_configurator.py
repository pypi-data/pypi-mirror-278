#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>
"""
This utility flashes the MCU with the new firmware
and then uploads the new set of parameters from yaml file
"""

import argparse
import logging
from autopilot_tools.enums import Devices
from autopilot_tools.px4.firmware_uploader import upload_firmware
from autopilot_tools.configurator.configurator import configure_params

logger = logging.getLogger(__name__)

def run_configurator():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('--firmware', type=str,
                        help='path/link to the firmware file')
    parser.add_argument('--config', type=str, nargs='+', metavar='FW',
                        help='Upload those set(s) of parameters to the MCU')
    parser.add_argument('-d', '--device', choices=Devices, type=str, default='serial',
                        help='either udp (SITL) or serial (HITL)')
    parser.add_argument('-f', '--force-calibrate', action='store_true',
                        help='set this flag to force calibration')
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    logger.setLevel(logging.INFO if args.verbose else logging.CRITICAL)

    if args.firmware is not None:
        upload_firmware(firmware=args.firmware)
    if args.config:
        configure_params(args.config, args.device, args.force_calibrate)
    if args.firmware is None and args.config is None:
        parser.error('Nothing to do! Please provide either --firmware or --config')

if __name__ == '__main__':
    run_configurator()

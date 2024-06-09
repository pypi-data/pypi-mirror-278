#!/usr/bin/env python3
# This program is free software under the GNU General Public License v3.
# See <https://www.gnu.org/licenses/> for details.
# Author: Dmitry Ponomarev <ponomarevda96@gmail.com>
# Author: Yuriy <1budsmoker1@gmail.com>

import os
from autopilot_tools.vehicle import Vehicle

def configure_params(config_pathes: list, device: str, force_calibrate: bool):
    assert isinstance(config_pathes, list)
    assert isinstance(device, str)
    assert isinstance(force_calibrate, bool)

    for idx, path in enumerate(config_pathes):
        assert isinstance(path, str), f"Element at index {idx} is not a string: {path}"

        if not os.path.isabs(path):
            config_pathes[idx] = os.path.abspath(path)

        assert os.path.isfile(config_pathes[idx]), f"File does not exist: {config_pathes[idx]}"

    vehicle = Vehicle()
    vehicle.connect(device)

    vehicle.reset_params_to_default()
    for config_path in config_pathes:
        vehicle.configure(config_path, reboot=True)

    if force_calibrate:
        vehicle.force_calibrate()
        vehicle.reboot()

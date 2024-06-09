# PX4/ArduPilot Autopilot tools [![](https://badge.fury.io/py/autopilot-tools.svg)](https://pypi.org/project/autopilot-tools/) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/build_package.yml/badge.svg) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/pylint.yml/badge.svg) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/tests.yml/badge.svg)

[autopilot_tools](https://pypi.org/project/autopilot-tools/) is a python package intended to be used as part of automated work with PX4 and Ardupilot autopilots such as hardware configuration, test scenarious providing and log analysis.

After the installation the package is accessible as a few executables:

1. `autopilot-configurator` uploads the given firmware to the autopilot, reset paramters to default, upload the required parameters and perform force sensor calibration.

    <img src="https://github.com/PonomarevDA/autopilot_tools/blob/docs/assets/autopilot_configurator.gif?raw=true" width="768">

2. `test-scenario` uploads the given mission to the autopilot, run it and wait until it is finished, then download the log from the vehicle and upload it to [review.px4.io](https://review.px4.io/). It returns a user the result of the flight and link to the flight report.

    <img src="https://github.com/PonomarevDA/autopilot_tools/blob/docs/assets/test_scenario.gif?raw=true" width="768">

Beside it the package allows to perform every step from a python script in a more customized way and to perform specific flight log analysis and to analyze an overall flight statistic based on multiple flight logs (total number of vehicle flight hours, flight distance, etc).

## 1. User guide

### 1.1. Installation

The package is distrubuted via [pypi.org/project/autopilot-tools/](https://pypi.org/project/autopilot-tools/).

```bash
pip install autopilot_tools
```

### 1.2. Using as executables

After the installation, a few executables will appear:
- autopilot-configurator
- test-scenario

For usage details run them with `--help` option or refer to the corresponded README.md: [src/autopilot_tools/utilities](src/autopilot_tools/utilities).

### 1.3. Using as a module

The package can be imported as a module. This allows you to implement more customized behaviour and use extended features if you need.

An example is shown below:

```python
from autopilot_tools.vehicle import Vehicle
from autopilot_tools.analyzer import Analyzer

vehicle = Vehicle()
vehicle.connect(device="serial")
vehicle.upload_firmware(firmware_path_or_url)
vehicle.configure(params_path)
vehicle.load_mission(mission_path)

res = vehicle.run_mission(mission_path)
print(res)

log_file = vehicle.load_latest_log(mission_path)

analzyer = Analyzer()
res = analzyer.analyse_log(log_file, analyze_requests=("airspeed", "ice", "esc_status"))
print(res)
```

## 2. Developer guide

### 2.1. Installation from sources

For a developer it is expected to use the package in [Development Mode (a.k.a. “Editable Installs”)](https://setuptools.pypa.io/en/latest/userguide/development_mode.html)

Clone the repository, install the package in development mode and use it in virtual environment:

```bash
git clone https://github.com/PonomarevDA/autopilot_tools.git
python3 -m venv venv
./venv/bin/activate
pip install -e .
```

### 2.2. Deployment

Please, deploy initially on [test.pypi.org](https://test.pypi.org/project/autopilot-tools/). Only if everything is fine, then deploy on [pypi.org](https://pypi.org/project/autopilot-tools/).

Try the script below to get details:

```bash
./deploy.sh --help
```

## 3. License

The package is distributed under MIT license.

# Skaff Telemetry

## Description 

The skaff_telemetry module is designed to enhance accelerator monitoring by sending HTTPS 
requests to a specified backend each time a function is invoked with the decorator. 
This capability is particularly useful for applications that require real-time monitoring 
or logging of function usage.

## Installation

To get started with the module, install it using pip, the Python package installer. 
This will download and install the module along with any necessary dependencies automatically.

```
$ pip install git+https://github.com/artefactory-skaff/python-skaff-probe
```

The decorator code is put into `skaff_telemetry/decorator.py`.

## Usage

Integrating sonde into your accelerator is straightforward. First, import the decorator 
from the module. Then, apply the sonde decorator above any function you wish to monitor.
 Each time the decorated function is called, sonde will send an HTTPS request 
 to your configured backend, allowing you to track when and how often the function is used.

An example is given in `skaff_telemetry/example.py` 

The following arguments must passed to the decorator:
- `accelerator_name`: name of the accelerator
- `version_number`: version of the accelerator
- `project_name`: if accessible, pass the name of the project in which the accelator will
be used.


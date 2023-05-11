# dnac_ap_heights

This tool searches the Cisco DNA Center for AccessPoints and changes their height to a defined value.

## Usage

### Install environment

This tool uses Python3.9
Install the environment with `pipenv install` and activate it with `pipenv shell`

### Configure tool

-   Add DNAC URL, username and password to `./input_files/device_credentials.py`
-   Configure required height in ft with the parameter `floor_height` in `./input_files/list_floors.py`
-   To use the tool on specific floors only, add floor ids to the parameter `floor_inputs` in `./input_files/list_floors.py`,
    to use on all floors, do not change `floor_inputs`

#### example configuration file `./input_files/device_credentials.py`

```
#!/usr/bin/env python

#to run scripts add dna center hostname and device credentials
device = {
			"hostname": "my_host",
			"user": "my_user",
			"pass": "my_password"
		}

```

#### example configuration file `./input_files/list_floors.py`

```
#!/usr/bin/env python

floor_height = "10"
floor_inputs = [

]
```

### Execute tool

Execute with `python DNAC_change_AP_height.py`

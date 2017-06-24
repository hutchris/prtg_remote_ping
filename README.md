# prtg_remote_ping
Scripts for remote pinging from various network device models.

Uses the netmiko library: https://github.com/ktbyers/netmiko

This project is made so that prtg can monitor whether a device can ping an IP address. PRTG's built in SSH Remote Ping sensor is very good if your monitored device is a linux based OS.

The benefit of this project is that it can be modified very easily to parse different ping outputs as well as customising the ping command parameters. For example, the reason this script started was the need to add vrf parameters to a ping command.

To get started you need to install netmiko and all of its prerequisites to the python instance that comes with PRTG. I recommend installing pip by downloaded the get-pip.py file from here https://pip.pypa.io/en/stable/installing/ then running

`
C:\Program Files (x86)\PRTG Network Monitor\Python34\python.exe" get-pip.py
`

Once you have pip you need to install netmiko. Open cmd as admin, then run:

`
C:\Program Files (x86)\PRTG Network Monitor\Python34\Scripts\pip.exe install netmiko
`

Warning - if you upgrade PRTG you may need to reinstall this package.

Now copy the remote_ping.py and the remote_ping_x.py files where x is the device model you are using. Paste them into the PRTG custom sensors directory: C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python

They should now be visible in the settings when you are creating a new "Python Script Advanced" sensor. remote_ping.py should not be selected for the sensor, but it needs to be in the directory to provide base code for the other files.

You need to have Linux credentials configured for the device and select "Transmit Linux Credentials" when creating the sensor.

The remote ping details go in the "Additional Parameters" field. It uses a key-values to pass parameters to the script. Seperate key-value pairs with a comma and seperate the key-values with a colon (no unnecessary spaces). The ping value is the remote IP that the device will ping, it is (obviously) a required parameter. params is optional.

ping:127.0.0.1,params:count 2

Let me know of any issues or if you would like a particular device model added. (needs netmiko support)

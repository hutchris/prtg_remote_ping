from netmiko import ConnectHandler
from paepy.ChannelDefinition import CustomSensorResult
import sys
import json

class NetmikoSensor(CustomSensorResult):
    def __init__(self,deviceType,sensor_message="OK"):
        self.channels = []
        self.has_error = False
        self.sensor_message = sensor_message
        self.deviceType = deviceType
        self.netConnect = None
        
    def writeError(self,errorStr):
        self.add_error(errorStr)
        print(self.get_json_result())
        if self.netConnect is not None:
            self.netConnect.disconnect()
        sys.exit()
        
    def parseArgs(self,params):
        data = json.loads(params)
        self.host = data['host']
        self.username = data['linuxloginusername']
        self.password = data['linuxloginpassword']
        self.rawArguments = data['params'].split(",")
        self.arguments = {}
        for argument in self.rawArguments:
            name = argument.split(":")[0]
            value = argument.split(":")[1]
            self.arguments[name] = value
            
    def connectDevice(self,delay=1,timeout=60,maxAttempts=3):
        while maxAttempts > 0 and self.netConnect is None:
        #for attempts that are not the final, supress error and increase delay/timeout
            try:
                device = {
                    "device_type":self.deviceType,
                    "ip":self.host,
                    "username":self.username,
                    "password":self.password,
                    "global_delay_factor":delay,
                    "timeout":timeout
                }
                self.netConnect = ConnectHandler(**device)
            except Exception as err:
                maxAttempts -= 1
                delay += 1
                timeout += 10
                if maxAttempts == 1:
                    self.writeError(errorStr="Failed to connect to device. {e}".format(e=str(err)))
                
    def sendCommand(self,cmdStr,maxAttempts=3):
        output = None
        while maxAttempts > 0 and output is None:
            try:
                output = self.netConnect.send_command(cmdStr)
            except Exception as err:
                maxAttempts -= 1
                self.netConnect.global_delay_factor += 1
                self.netConnect.timeout += 10
                if maxAttempts == 1:
                    self.writeError("Device connected but send command failed. {e}".format(e=str(err)))
        return(output)

from remote_ping import NetmikoSensor
import sys

class CiscoSensor(NetmikoSensor):
    def parsePing(self,rawPing):
        if "!" in rawPing:
            try:
                pingOutputLines = rawPing.split("\n")
                stats = [line for line in pingOutputLines if "min/avg/max" in line][0].strip().split(" ")[-2].split("/")
                results = {
                    "Minumum Response":float(stats[0]),
                    "Average Response":float(stats[1]),
                    "Maximum Response":float(stats[2]),
                }
            except Exception as err:
                self.writeError("Error parsing ping output. {e}. {o}.".format(e=str(err),o=rawPing))
        else:
            sensor.writeError("Remote ping failed. Raw ping result: {pr}".format(pr=rawPing))
        return(results)

if __name__ == "__main__":
    try:
        sensor = CiscoSensor(deviceType="cisco_ios")
        sensor.parseArgs(sys.argv[1])
        sensor.connectDevice()
        pingOutput = sensor.ping()
        output = sensor.parsePing(pingOutput)
        for name,result in output.items():
            sensor.add_channel(channel_name=name,value=result,unit="TimeResponse")
        sensor.sensor_message = "Ping: {ip} OK".format(ip=sensor.arguments['ping'])
        print(sensor.get_json_result())
        sensor.netConnect.disconnect()
    except Exception as err:
        sensor.writeError("Error. {e}".format(e=str(err)))



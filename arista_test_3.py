


import json
import requests
import sys
from requests.auth import HTTPBasicAuth 


#devices = ['192.168.56.102','192.168.56.103']
def config_temp(device, commands):
	url = 'http://{}/command-api'.format(device)
	auth = HTTPBasicAuth('admin','admin')
	payload = {
         "jsonrpc": "2.0",
         "method": "runCmds",
         "params": {
            "format": "json",
            "timestamps": False,
            "cmds":commands ,
            "version": 1
            },
            "id": "EapiExplorer-1"
        }
	response = requests.post(url, data=json.dumps(payload), auth=auth)
	return json.loads(response.text)

def lldp_nei(device):
	commands = ['show lldp neighbors']
	response = config_temp(device, commands)
	neighbors = response['result'][0]['lldpNeighbors']
	return (neighbors)
	#return neighbors

def config_interfaces(device, neighbors):
	command_list=['enable','configure']
	for neighbor in neighbors:
		def_route = 'ip route 0.0.0.0 0.0.0.0 Management 1'
		local_interface = neighbor['port']
		print (local_interface)
		if local_interface.startswith('Eth'):
			description = 'Connected to port {} of {}' .format(neighbor['neighborPort'], neighbor['neighborDevice']) 
			description = 'description ' + description
			interface = 'interface {}'.format(local_interface)
			cmds = [def_route, interface, description]
		command_list.extend(cmds)
	response = config_temp(device, command_list)
	print (response)

if __name__ == "__main__":
	devices = ['192.168.56.102','192.168.56.103']
	for device in devices:
		neighbors = lldp_nei(device)
		config_interfaces (device, neighbors)

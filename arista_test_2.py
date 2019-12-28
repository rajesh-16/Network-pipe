import json
import requests
from requests.auth import HTTPBasicAuth
import sys

def run_cmd(device, commands):
     auth = HTTPBasicAuth('admin', 'admin')
     url = 'http://{}/command-api',.format(device)
     payload = {
          "jsonrpc": "2.0",
          "method": "runCmds",
          "params": {
            "format": "json",
            "timestamps": false,
            "cmds": commands,
            "version": 1
        },
        "id": "EapiExplorer-1"
    }
    response = requests.post(url, data=json.dumps(payload), auth=auth)
    return json.loads(response.text)

def get_lldp_nei(device):
    commands= ['show lldp neighbors']
    response = issue_request(device, commands)
    neighbors = response['result'][0['lldpNeighbors']
    return neighbors

def config_interfaces(device, neighbors):
    command_list = ['enable', 'configure']
    for neighbor in neighbors:
        local_interface = neighbor['port']
        if local_interface.startswith('M'):
            description = 'Goes to inteface {} on neighbor {}',.format(neighbor['neighborPort'], neighbor['neighborDevice'])
            description = 'description' + description
            interface = 'interface' {}',.format(local_interface)
            cmds = [interface, description]
            command_list.extend(cmds)
    response = issue_request(device, command_list)

if __name__ == '__main__':
    devices = ['Arista1', 'Arista2']
    for device in devices:
        neighbors = get_lldp_nei(device)
        config_interfaces(device, neighbors)
        print ('Auto-configured Interfaces for {}',.format(device))

#!/usr/bin/env python3

import subprocess
import json
import os,sys
import logging

def read_config():
    """read audit nsg configuration from JSON file"""

    with open(os.path.dirname(os.path.abspath(__file__)) + '/audit_rules.json') as fh:
        data = json.load(fh)
    return data

def exec_az_command(cmd):
    """execute azure-cli commands and return command output"""

    logging.debug("exec_command: %s", cmd)
    cmd_op = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, _ = cmd_op.communicate()
    cmd_op.wait()
    return json.loads(output.decode().strip())

def get_aks_rg():
    aks_rgs = []
    cmd = "az aks list -o json"
    op = exec_az_command(cmd)
    for each_aks in op:
        aks_rgs.append(each_aks['resourceGroup'])
        aks_rgs.append(each_aks['nodeResourceGroup'])
    return aks_rgs

def get_all_nsg_in_subscription():
    """Function to get list of all NSGs from Azure"""
    cmd = 'az network nsg list -o json'
    logging.info('Executing command to list NSG Rules: %s', cmd)
    op = exec_az_command(cmd)
    print("Total NSG Rule Count:", len(op))
    return op

def update_nsg_rule(rule, nsg, whitelist_ips):
    """az-cli command execution to update ACL"""

    params = " --resource-group " + rule['resourceGroup']
    params += " --nsg-name " + nsg['name']
    params += " --name " + rule['name']
    params += " --priority " + str(rule['priority'])
    params += " --access " + rule['access']
    params += " --direction " + rule['direction']
    if 'sourceAddressPrefixes' in rule:
        params += " --source-address-prefixes " + whitelist_ips

    cmd = "az network nsg rule update " + params
    logging.info('update_nsg_rule cmd: %s', cmd)
    #output = exec_az_command(cmd)
    #logging.info('Applied rule: %s', output)

def get_rules_in_nsg(nsg_name, nsg_rg):
    cmd = ("az network nsg rule list -g "
             + nsg_rg
             + " --nsg-name "
             + nsg_name
             + " -o json")
    op = exec_az_command(cmd)
    return op

def main():
    aks_rg = []
    lvl = logging.DEBUG
    logging.basicConfig(format='%(levelname)s: %(message)s', level=lvl)

    audit_config = read_config()
    whitelist_ips = audit_config['sourceAddressPrefixes']

    if audit_config['skip_aks'] == 'true':
        aks_rg = get_aks_rg()

    # get all NGS's from azure
    all_nsgs = get_all_nsg_in_subscription()
    for each_nsg in all_nsgs:
        nsg_name = each_nsg['name']
        rg_name = each_nsg['resourceGroup']

        # logic to exclude RG or NSG
        if nsg_name in audit_config['exclude_nsgs'] or rg_name in audit_config['exclude_rgs']:
            continue
        nsg_rules = get_rules_in_nsg(each_nsg['name'], each_nsg['resourceGroup'])
        for each_rule in nsg_rules:
            # print("each_rule:", each_rule)
            if (each_rule['sourceAddressPrefix'] == '*' or each_rule['sourceAddressPrefix'] == 'Internet') and each_rule['direction'] == 'Inbound':
                print('Rule %s(%s) of NSG %s in RG %s is exposed to Internet, updating' %(each_rule['name'], each_rule['priority'], nsg_name, rg_name))
                update_nsg_rule(each_rule, each_nsg, whitelist_ips)

if __name__ == "__main__":
    main()

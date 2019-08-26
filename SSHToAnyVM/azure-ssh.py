#!/usr/bin/env python

import logging
import click
import sys
import os
import json
import getpass
import subprocess

def exec_az_command(az_cmd):
    #click.echo('Executing Azure command: {}'.format(az_cmd))
    output = ""
    try:
        cmd_op = subprocess.Popen(az_cmd, stdout=subprocess.PIPE, shell=True)
        output, err = cmd_op.communicate()
        cmd_op.wait()
        output = json.loads(output.decode().strip())
    except:
        click.secho('Could not execute az cli command ({})'.format(az_cmd), fg='red')
    return output

def ssh_to_azure_vm(vm_name, rg):
    user_ssh_key = os.path.expanduser('~/.ssh/id_rsa.pub')
    user_name = getpass.getuser()

    cmd = 'az vm show -n ' + vm_name + ' -g ' + rg + ' -o json'
    vm_details = exec_az_command(cmd)
    if vm_details:
        vm_nic = vm_details['networkProfile']['networkInterfaces'][0]['id'].split('/')[-1]
        vm_location = vm_details['location']
        cmd = 'az network nic ip-config list --nic-name ' + vm_nic + ' -g ' + rg + ' -o json'
    else:
        click.secho('Could not get NIC details attached to VM {}'.format(vm_name), fg='red')
        sys.exit(-1)

    nic_ip_config = exec_az_command(cmd)
    ip_config_name = nic_ip_config[0]['name']
    click.echo('IP Config name associated with VMs NIC: {}'.format(ip_config_name))
    pub_ip_name = user_name + '-debug-pub-ip'
    cmd = 'az network public-ip create -n ' + pub_ip_name + ' -g ' + rg + ' -l ' + vm_location + ' -o json'
    pub_ip_details = exec_az_command(cmd)
    click.echo('Updating Azure VM with local user({}) and SSH key({})'.format(user_name, user_ssh_key))
    if os.path.isfile(user_ssh_key):
        cmd = 'az vm user update -u ' + user_name + ' --ssh-key-value ' + user_ssh_key + ' -n ' + vm_name + ' -g ' + rg + ' -o json'
    else:
        click.secho('SSH Public Key not found for user {}'.format(user_name), fg='red')
        sys.exit(-1)

    vm_update_creds = exec_az_command(cmd)
    click.echo('Updated local user and SSH key to VM {}'.format(vm_name))
    if ip_config_name:
        cmd = 'az network nic ip-config update -n ' + ip_config_name + ' -g ' + rg + ' --nic-name ' + vm_nic + ' --public-ip-address ' + pub_ip_name
    else:
        click.secho('Could not get IP Config name associated with VMs NIC', fg='red')
        sys.exit(-1)

    vm_update_pub_ip = exec_az_command(cmd)
    click.echo('Updated {} VM NIC with public IP'.format(vm_name))
    cmd = 'az network public-ip show -n ' + pub_ip_name + ' -g ' + rg + ' -o json'
    vm_pub_ip = exec_az_command(cmd)
    pub_ip = vm_pub_ip['ipAddress']
    click.echo('Attached IP {}({}) to VM {} NIC'.format(pub_ip, pub_ip_name, vm_name))
    click.echo('VM ready for SSH! Enjoy!!')
    click.echo('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+')
    click.echo('MAKE SURE PROPER NSG IS CONFIGURED TO ALLOW SSH')
    click.echo('Command to SSH to VM:\n\tssh {}@{}'.format(user_name, pub_ip))
    click.echo('Command to get root shell:\n\tsudo -i')
    del_ip = 'az network public-ip delete -n ' + pub_ip_name + ' -g ' + rg
    del_ip_association = 'az network nic ip-config update -g ' + rg + ' --nic-name ' + vm_nic + ' -n ' + ip_config_name + ' --remove publicIpAddress'
    click.echo('Command to disassociate IP Address with NIC (save cost!):\n\t{}'.format(del_ip_association))
    click.echo('Command to delete IP Address resource:\n\t{}'.format(del_ip))
    click.echo('+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+')

@click.command()
@click.option('--name', '-n', required=True, help='Azure VM Name')
@click.option('--rg', '-g', required=True, help='Azure VM Resource Group')
def azure_ssh(name, rg):
    """SSH to Azure VM/Node"""
    click.echo('Preparing VM {} in resource group {} for SSH Connection'.format(name, rg))
    ssh_to_azure_vm(name, rg)

if __name__ == '__main__':
    azure_ssh()

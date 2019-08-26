# Script to enable SSH on any VM
Tested the script on MacOS, should work on any *nix systems

# Usage
```
$ ./azure-ssh.py --help
Usage: azure-ssh.py [OPTIONS]

  SSH to Azure VM/Node

Options:
  -n, --name TEXT  Azure VM Name  [required]
  -g, --rg TEXT    Azure VM Resource Group  [required]
  --help           Show this message and exit.
```

# Execution
```
$ ./azure-ssh.py -n praveend-test-vm-cpu-worker-7586d4c89-kq7gg -g praveend-test-vm
Preparing VM praveend-test-vm-cpu-worker-7586d4c89-kq7gg in resource group praveend-test-vm for SSH Connection
IP Config name associated with VMs NIC: praveend-test-vm-cpu-worker-7586d4c89-kq7gg-nic
Updating Azure VM with local user(pdarshanam) and SSH key(/Users/pdarshanam/.ssh/id_rsa.pub)
Updated local user and SSH key to VM praveend-test-vm-cpu-worker-7586d4c89-kq7gg
#!/usr/bin/env python
Updated praveend-test-vm-cpu-worker-7586d4c89-kq7gg VM NIC with public IP
Attached IP 13.xx.yy.209(pdarshanam-debug-pub-ip) to VM praveend-test-vm-cpu-worker-7586d4c89-kq7gg NIC
VM ready for SSH! Enjoy!!
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
MAKE SURE PROPER NSG IS CONFIGURED TO ALLOW SSH
Command to SSH to VM:
	ssh pdarshanam@13.xx.yy.209
Command to get root shell:
	sudo -i
Command to disassociate IP Address with NIC (save cost!):
	az network nic ip-config update -g praveend-test-vm --nic-name praveend-test-vm-cpu-worker-7586d4c89-kq7gg-nic -n praveend-test-vm-cpu-worker-7586d4c89-kq7gg-nic --remove publicIpAddress
# Script to enable SSH on any VM
Command to delete IP Address resource:
	az network public-ip delete -n pdarshanam-debug-pub-ip -g praveend-test-vm
+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
```

# SSH to VM
```
$ ssh pdarshanam@13.xx.yy.209
The authenticity of host '13.xx.yy.209 (13.xx.yy.209)' can't be established.
ECDSA key fingerprint is SHA256:Spcv4/JPWFd9jGIXHDmwBsDX/I4f0WXf5+t/xCwqiB8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '13.xx.yy.209' (ECDSA) to the list of known hosts.
Container Linux by CoreOS stable (2079.4.0)
Update Strategy: No Reboots
pdarshanam@praveend-test-vm-cpu-worker-7586d4c89-kq7gg ~ $ logout
Connection to 13.xx.yy.209 closed.
```

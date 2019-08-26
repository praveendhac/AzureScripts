#!/usr/bin/env python3

import os, sys
import argparse
import subprocess
import json

# az ad user create --display-name "Remove Me" --password Removem3 --user-principal-name removeme@example.onmicrosoft.com
# az ad user delete --upn-or-object-id removeme@example.onmicrosoft.com
# az role assignment create --assignee aa69b9fc-5a24-4bcd-9e7d-137d9cc15cc0 --role reader
# az role assignment delete --assignee aa69b9fc-5a24-4bcd-9e7d-137d9cc15cc0

def add_role(objectId, role):
  cmd = "az role assignment create --assignee " + objectId + " --role " + role
  print(cmd)
  add_role_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
  if not add_role_result.stderr:
    print(add_role_result.stdout.decode('utf-8'))

def add_user(args):
  password = "Removem3"
  username = args.username + "@example.onmicrosoft.com"

  print("Adding user to Azure Active directory:", username)
  if args.fullname:
    print("Full Name:", args.fullname)
    cmd = "az ad user create --display-name \"" + args.fullname + "\" --password " + password + " --user-principal-name " + username + " --force-change-password-next-login"
  else:
    cmd = "az ad user create --display-name " + args.username + " --password " + password + " --user-principal-name " + username + " --force-change-password-next-login"

  print("CMD:", cmd)
  add_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
  if not add_result.stderr:
    user_details = json.loads(add_result.stdout.decode('utf-8'))
    print("objectId:", user_details['objectId'])
    print("userPrincipalName:", user_details['userPrincipalName'])
    #print(user_details[''])
    print(add_result.stdout.decode('utf-8'))
  else:
    print("ADD ERROR:\n", add_result.stderr.decode('utf-8'))
    sys.exit(-1)
  if args.role:
    oid = user_details['objectId']
    pn = user_details['userPrincipalName']
    role = args.role
    add_role(oid, role)

def list_users():
  print("Listing users\n")
  cmd = "az ad user list -o table"
  print("CMD:", cmd)
  list_users = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
  if not list_users.stderr:
    print(list_users.stdout.decode('utf-8'))
  else:
    print(list_users.stderr.decode('utf-8'))

def delete_user(args):
  cmd = "az ad user delete --upn-or-object-id " + args.delete
  print("CMD:", cmd)
  del_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
  if not del_result.stderr:
    print(del_result.stdout.decode('utf-8'))
  else:
    print("ERROR:\n", del_result.stderr.decode('utf-8'))

def list_guest_users(args):
  print("Getting Guest users list")
  print("ags:", args)
  cmd = "az ad group list -o json"
  print("CMD:", cmd)
  group_list = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
  if group_list.stderr:
    print("ERROR:\n", group_list.stderr.decode('utf-8'))
    return
  aad_grps = json.loads(group_list.stdout)
  for each_grp in aad_grps:
    #print(each_grp['displayName'], each_grp['objectId'], each_grp['description'])
    cmd = "az ad group member list -g " + each_grp['objectId'] + " -o table"
    print("CMD:", cmd)
    grp_members = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
    if grp_members.stderr:
      print("ERROR:\n", grp_members.stderr.decode('utf-8'))
      continue
    print(grp_members.stdout.decode('utf-8'))
    #aad_grps = json.loads(grp_members.stdout)
    #for each_user in aad_grps:
    #  print("each_user:", each_user)
def usage(p):
    p.print_help()
    print("\nCreate user (pdarshanam@example.onmicrosoft.com) with contributor role e.g.")
    print("%s -f \"Praveen Darshanam\" -u pdarshanam -r contributor" %(sys.argv[0]))
    sys.exit(-1)

def main():
  prog_name = sys.argv[0]
  parser = argparse.ArgumentParser(prog = prog_name, description='Manage users on Azure Active Diretory')
  #parser.add_argument('-c', '--create', help='Create User', choices=["-u"])
  parser.add_argument('-d', '--delete', help='Delete User, The object ID or principal name of the user to delete')
  parser.add_argument('-f', '--fullname', help='User Full name')
  parser.add_argument('-g', '--guestusers', help='list guest users')
  parser.add_argument('-u', '--username', help='[Required]: Add user, domain \"example.onmicrosoft.com\" will be automatically added')
  parser.add_argument('-l', '--list', help='List all Users', action="store_true")
  parser.add_argument('-r', '--role', help='Add Role')
  args = parser.parse_args()

  if args.username:
    add_user(args)
  elif args.list:
    list_users()
  elif args.delete:
    delete_user(args)
  elif args.role:
    if not args.username:
      print("username is mandatory")
      usage(parser) 
  elif args.guestusers:
    list_guest_users(args)
  else:
    usage(parser) 

if __name__ == "__main__":
  main()

# Manage AAD USers

# Usage
```
$ ./add_user.py
usage: ./add_user.py [-h] [-d DELETE] [-f FULLNAME] [-g GUESTUSERS]
                     [-u USERNAME] [-l] [-r ROLE]

Manage users on Azure Active Diretory

optional arguments:
  -h, --help            show this help message and exit
  -d DELETE, --delete DELETE
                        Delete User, The object ID or principal name of the
                        user to delete
  -f FULLNAME, --fullname FULLNAME
                        User Full name
  -g GUESTUSERS, --guestusers GUESTUSERS
                        list guest users
  -u USERNAME, --username USERNAME
                        [Required]: Add user, domain "example.onmicrosoft.com"
                        will be automatically added
  -l, --list            List all Users
  -r ROLE, --role ROLE  Add Role

Create user (pdarshanam@example.onmicrosoft.com) with contributor role e.g.
./add_user.py -f "Praveen Darshanam" -u pdarshanam -r contributor
```

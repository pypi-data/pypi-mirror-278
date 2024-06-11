


import grp

def list_groups():
    groups = grp.getgrall()
    group_list = [group.gr_name for group in groups]
    return group_list

# Usage
groups = list_groups()
for group in groups:
    print(group)

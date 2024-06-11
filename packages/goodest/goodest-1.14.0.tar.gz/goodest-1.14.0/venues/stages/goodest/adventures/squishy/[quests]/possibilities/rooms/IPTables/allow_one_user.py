


'''
useradd -m -s /bin/bash communicator
passwd communicator # EEC1234

iptables -A OUTPUT -m owner --uid-owner communicator -j ACCEPT

sudo -u communicator firefox

'''
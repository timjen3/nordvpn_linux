# About
Determines your geographical location based on current ip address and calculates the closest NordVPN server with least load to connect to. Does a series of ping tests to ensure it has a good response time.

You can specify a few configuration options in tool.json
1. required_categories:
"Standard VPN servers", "P2P", "Onion over VPN", "Double VPN", "Anti DDoS", "Dedicated IP servers", "Obfuscated Servers"

2. required_search_keywords:
Not sure the whole list, but I am curious if "Netflix" will actually work with Netflix. Not yet tried.

3. openvpn command line arguments can be put into tool.json as well. There are some defaults in there.

# Prerequesites

Added a script called prereqs.sh that is untested and will require some tinkering. But it's real simple stuff so don't feel too stressed.

Trying my best to get rid of the terminal window. The only way I've been able to do it is to add my user to the vpnusers group and add this line to /etc/sudoers:
%vpnusers ALL = NOPASSWD: /usr/sbin/openvpn

WARNING: Be extremely careful with the sudoers file. If you mess this file up you will have to go into linux recovery mode to fix the file1!!

# Notes

There are 3 external sources used by this tool that can be adjusted. If these stop working you can swap them out fairly easily although some will take more work.

1. Currently using api.nordvpn.com/server but I have ran into http://zwyr157wwiu6eior.com/server and might use as backup.
1. URL for determining WAN IP is hardcoded.
1. URL for determining locale information is hardcoded.

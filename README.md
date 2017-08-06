# About
Determines your geographical location based on current ip address and calculates the closest NordVPN server with least load to connect to. Does a series of ping tests to ensure it has a good response time.

You can specify a few configuration options in tool.json
1. required_categories:
"Standard VPN servers", "P2P", "Onion over VPN", "Double VPN", "Anti DDoS", "Dedicated IP servers", "Obfuscated Servers"

2. required_search_keywords:
Not sure the whole list, but I am curious if "Netflix" will actually work with Netflix. Not yet tried.

3. openvpn command line arguments in tool.json as well. There are some defaults in there.

TODO: Add better way to start / stop.

# Prerequesites

1. Install openvpn
1. Install python 3.x no additional packages needed.

# Getting Started


# Notes

There are 3 external sources used by this tool that can be adjusted. If these stop working you can swap them out fairly easily although some will take more work.

1. Currently using api.nordvpn.com/server but I have ran into http://zwyr157wwiu6eior.com/server and might use as backup.
1. URL for determining WAN IP is hardcoded.
1. URL for determining locale information is hardcoded.

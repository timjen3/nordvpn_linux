# About
Determines your geographical location based on current ip address and calculates the closest NordVPN server to connect to.

You can specify a few configuration options in tool.json
1. required_categories:
"Standard VPN servers", "P2P", "Onion over VPN", "Double VPN", "Anti DDoS", "Dedicated IP servers", "Obfuscated Servers"

2. required_search_keywords:
Not sure the whole list, but I am curious if "Netflix" will actually work with Netflix. Not yet tried.

3. openvpn command line arguments in tool.json as well. There are some defaults in there.

TODO: Add better way to start / stop.
TODO: Server speeds seem to vary a lot... Add a means to check server quality before choosing one.
TODO: Download and unzip NordVPN ovpn files to avoid the manual step.

# Prerequesites

1. Install openvpn
1. Install python 3.x no additional packages needed.

# Getting Started

1. Clone this repository.
1. Download and unzip the nordvpn ovpn files to content/ovpnfiles
1. Create a file in the root directory of the cloned repository called 'auth.txt' with your nord username on line 1, your nord password on line 2, and no additional lines.

# Notes

There are 3 external sources used by this tool that can be adjusted. If these stop working you can swap them out fairly easily although some will take more work.

1. Currently using api.nordvpn.com/server but I have ran into http://zwyr157wwiu6eior.com/server and might use as backup.
1. The URL that provides the WAN IP for your machine is hardcoded.
1. The URL that provides locale information about your WAN IP is hardcoded as well.

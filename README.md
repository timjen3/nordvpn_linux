# About

Not yet tried in production.

# Prerequesites

1. Install openvpn
1. Install python 3.x no additional packages needed.


# Getting Started

1. Clone this repository.
1. Download and unzip the nordvpn ovpn files to content/ovpnfiles
1. Create a file in the root directory of the cloned repository called 'auth.txt' with your nord username on line 1, your nord password on line 2, and no additional lines.

# Future

TODO: Add code to set this up as an init.d service.

TODO: Add code to download and unzip NordVPN ovpn files to avoid the manual step.

There are 3 external sources used by this tool that can be adjusted. If these stop working you can swap them out fairly easily although some will take more work.

1. NordVPN doesn't officially provide metadata for their servers, but I found one in the logs from the Windows application. If the url changes in the future it can be adjusted in tool.json
1. The URL that provides the WAN IP for your machine is hardcoded.
1. The URL that provides locale information about your WAN IP is hardcoded as well.

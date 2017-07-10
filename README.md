# nordvpn_linux

# Prerequesites

1. Install openvpn with the package manager available to your system.
1. Install python 3.x no additional packages needed.


# Getting Started

1. Clone this repository.
1. Download and unzip the nordvpn ovpn files to content/ovpnfiles

# Future

There are 3 external sources used by this tool that can be adjusted.

1. NordVPN doesn't officially provide metadata for their servers, but I found one in the logs from the Windows application. If the url changes in the future it can be adjusted in tool.json
1. The URL that provides the WAN IP for your machine is hardcoded.
1. The URL that provides locale information about your WAN IP is hardcoded as well.

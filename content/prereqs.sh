# nordvpn connector getting started helper; untested.

sudo apt-get install python3
sudo apt-get install openvpn
sudo apt-get install python3-tk


nordvpnusername=input "what's your nordvpn login email?"
nordvpnpassword=input "what's your nordvpn login password?"

cd /usr/src
git clone https://github.com/timjen3/nordvpn_linux
cd nordvpn_linux
$nordvpnusername\n > auth.txt
$nordvpnpassword > auth.txt
cd ..
echo "Installation complete."

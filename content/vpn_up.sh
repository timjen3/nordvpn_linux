# WARNING: This doesn't work, need to play around with it.

# Disable non-VPN traffic
sudo ufw default deny outgoing
sudo ufw default deny incoming

# Allow VPN pass through
sudo ufw allow out on tun0 from any to any
sudo ufw allow in on tun0 from any to any

# Allow VPN to connect
sudo ufw allow out 1194/udp
sudo ufw allow out 443/tcp

# Enable
sudo ufw enable

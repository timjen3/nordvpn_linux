# Disable non-VPN traffic
sudo ufw default deny outgoing
sudo ufw default deny incoming

# Allow VPN pass through
sudo ufw allow out on tun0 from any to any
sudo ufw allow in on tun0 from any to any

# Enable
sudo ufw enable

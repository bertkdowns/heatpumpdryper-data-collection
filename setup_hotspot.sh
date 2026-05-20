# Create a new hotspot connection
sudo nmcli con add type wifi ifname wlan0 mode ap con-name "RaspberryHotspot" ssid "RaspberryTips-WiFi"

# Set WPA2 encryption
sudo nmcli con modify "RaspberryHotspot" wifi-sec.key-mgmt wpa-psk
sudo nmcli con modify "RaspberryHotspot" wifi-sec.psk "MySecurePassword"

# 2.4 GHz band, channel 6
sudo nmcli con modify "RaspberryHotspot" 802-11-wireless.band bg
sudo nmcli con modify "RaspberryHotspot" 802-11-wireless.channel 6

# IP address of the Pi in the hotspot network (enable DHCP for clients)
sudo nmcli con modify "RaspberryHotspot" ipv4.method shared
sudo nmcli con modify "RaspberryHotspot" ipv4.address 192.168.4.1/24

# Disable IPv6
sudo nmcli con modify "RaspberryHotspot" ipv6.method disabled


# autoconnect on boot
sudo nmcli con modify "RaspberryHotspot" connection.autoconnect yes

# Start hotspot
sudo nmcli con down "RaspberryHotspot"
sudo nmcli con up "RaspberryHotspot"
# pywisam

A Wifi pentesting framework written in Python


## Options

- *Option 1*: Scan - Scan all the Wifi networks

- *Option 2*: Capture traffic (Airodump) - Capture traffic using Airodump

- *Option 3*: Crack handshake - Crack a pcap file containing a handshake using Aircrack

- *Option 4*: Deauth attack - Execute a deauthentication attack using Aireplay

- *Option 5*: Create AP - Create a Fake Access Point with any encryption: Open, WEP, WPA2, WPA2-Enterprise

- *Option 6*: Connect - Connect to a Wifi network

- *Option 7*: Get hidden ESSID - Attack a Wifi with the ESSID hidden to get the network name


# Example

![Screenshot](https://i.imgur.com/OlTzpbl.png)


## Requirements

```
apt-get install hostapd
```

Python 2.x:

```
pip install -r install/requirements.txt
```

Python 3.x:

```
pip3 install -r install/requirements.txt
```

## Note

Tested both in Python2.x (2.7.15rc1) and Python 3.x (3.6.7)

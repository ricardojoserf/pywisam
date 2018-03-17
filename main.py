#!/usr/bin/env python

import os
import sys
import time
from wifi import Cell, Scheme

#interfaz = 'wlxc04a00118487'
interfaz = raw_input('Network interface: ')
os.system("sudo ifconfig "+interfaz+" down")
os.system("sudo ifconfig "+interfaz+" up")
redes = []


def menu():
	opt_ = raw_input('\nOptions: \n1: Scan \n2: Connect \n3: Capture traffic\n4: Crack WPA/WPA2 traffic file \n5: Deauth AP \n6: Deauth specific client \n7: Create AP\n')
	if opt_ == "1":
		scan()
	elif opt_=="2":
		connect()
	elif opt_=="3":
		capture_traffic()
	elif opt_=="4":
		crack_wpa()
	elif opt_=="5":
		deauth_ap()
	elif opt_=="6":
		deauth_client()
	elif opt_=="7":
		create_ap()
	else:
		print "Unknown option"


def create_ap():
	ap_type=raw_input("Options: \n1: Open \n2: WPE \n3: WPA2\n")
	if ap_type == "1":
		essid=raw_input("Network name:")
		channel=raw_input("Channel:")
		print "Creating conf file in temp/"
		os.system("echo 'interface="+interfaz+"\ndriver=nl80211\nssid="+essid+"\nhw_mode=g\nchannel="+channel+"\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=0\nmacaddr_acl=1' > temp/open.conf")
		time.sleep(1)
		print "Deploying AP..."
		os.system("sudo hostapd temp/open.conf")
	if ap_type == "2":
		essid=raw_input("Network name:")
		passphrase = raw_input("Passphrase:")
		while ( len(passphrase)!=5 and len(passphrase)!=13 and len(passphrase)!=16 and len(passphrase)!=29):
			print "Incorrect length (5,13,16 or 29 characters)"
			passphrase = raw_input("Passphrase:")
		channel=raw_input("Channel:")
		print "Creating conf file in temp/"
		os.system("echo 'interface="+interfaz+"\ndriver=nl80211\nssid="+essid+"\nhw_mode=g\nchannel="+channel+"\nmacaddr_acl=0\nauth_algs=3\nignore_broadcast_ssid=0\nwep_default_key=1\nwep_key1=\""+passphrase+"\"\nwep_key_len_broadcast=\"5\"\nwep_key_len_unicast=\"5\"\nwep_rekey_period=300' > temp/wep.conf")
		time.sleep(1)
		print "Deploying AP..."
		os.system("sudo hostapd temp/wep.conf")
	if ap_type == "3":
		essid=raw_input("Network name:")
		passphrase = raw_input("Passphrase:")
		while len(passphrase)<8:
			print "Incorrect length (8 or more characters)"
			passphrase = raw_input("Passphrase:")
		channel=raw_input("Channel:")
		print "Creating conf file in temp/"
		os.system("echo 'interface="+interfaz+"\nssid="+essid+"\nchannel="+channel+"\nwpa_passphrase="+passphrase+"\nhw_mode=g\nieee80211n=1\nwmm_enabled=1\nauth_algs=1\nwpa=2 \nwpa_key_mgmt=WPA-PSK \nrsn_pairwise=CCMP' > temp/wpa.conf")
		time.sleep(1)
		print "Deploying AP..."
		os.system("sudo hostapd temp/wpa.conf")


def deauth_client():
	ap_mac = raw_input("AP MAC:")
	essid=raw_input("Network name:")
	channel=raw_input("Channel:")
	client_mac = raw_input("Client MAC:")
	os.system("sudo airmon-ng check kill")
	os.system("sudo airmon-ng start "+interfaz+" "+channel)
	interfaz_mon = raw_input("Monitorization interface:")
	os.system("sudo ifconfig "+interfaz+" down")
	os.system("aireplay-ng -0 0 -a "+ap_mac+"-c "+client_mac+" -e "+essid+" "+interfaz_mon)


def deauth_ap():
	ap_mac = raw_input("AP MAC:")
	essid=raw_input("Network name:")
	channel=raw_input("Channel:")
	os.system("sudo airmon-ng check kill")
	os.system("sudo airmon-ng start "+interfaz+" "+channel)
	interfaz_mon = raw_input("Monitorization interface:")
	os.system("sudo ifconfig "+interfaz+" down")
	os.system("aireplay-ng -0 0 -a "+ap_mac+" -e "+essid+" "+interfaz_mon)


def crack_wpa():
	dictionary = raw_input("Dictionary file: ")
	pcap_name = raw_input("Pcap file name: ")
	os.system("aircrack-ng -w "+dictionary+" "+pcap_name)


def capture_traffic():
	pcap_name = raw_input("Pcap file name: ")
	os.system("touch "+pcap_name)
	os.system("chmod 777 "+pcap_name)
	os.system("sudo tshark -w "+pcap_name+" -i "+interfaz)


def connect():
	id_red = raw_input('Select id: ')
	essid=redes[int(id_red)][0]
	conf_file="temp/supp.conf"

	is_psk = raw_input("Is WPA-PSK? (y/N)")
	if is_psk == "y":
		password = raw_input('Password: ')
		os.system( "wpa_passphrase "+essid+" "+password+" > " + conf_file)
		os.system("wpa_supplicant -Dnl80211 -i "+interfaz+" -c "+conf_file+" &")
		sys.exit()

	is_enterprise = raw_input("Is WPA-Enterprise? (y/N)")
	if is_enterprise == "y":
		identity = raw_input('Identity: ')
		password = raw_input('Password: ')
		is_mschapv2 = raw_input("Use PEAP+MSCHAPv2? (y/N)")
		if is_mschapv2 == "y":
			os.system("echo 'ctrl_interface=DIR=/var/run/wpa_supplicant \nnetwork={ \nssid=\""+essid+"\"\nscan_ssid=1 \nkey_mgmt=WPA-EAP \neap=PEAP \nidentity=\""+identity+"\"\npassword=\""+password+"\" \nphase1=\"peaplabel=0\" \nphase2=\"auth=MSCHAPV2\" \n}' > "+conf_file)
			os.system("wpa_supplicant -Dnl80211 -i "+interfaz+" -c "+conf_file+" &")


def scan():
	global redes
	list_ = []
	redes = []
	print "\nScanning...\n"
	while len(list_) == 0:
		list_ = Cell.all(interfaz)
	for i in list_:
		ssid = i.ssid
		mac = i.address
		frecuencia = i.frequency
		canal = i.channel
		max_rate= i.bitrates[len(i.bitrates)-1]
		if i.encrypted:
			cifrado = i.encryption_type
		else:
			cifrado = "None"
		redes.append( ( str(ssid), str(cifrado), str(mac), str(frecuencia), str(canal), str(max_rate) ) )
	count = 0
	for red in redes:
		print "- ", red[0],"(ID = ",count,")"
		print "   Info: ("+red[1]+", "+red[2]+", "+red[3]+", "+red[4]+", "+red[5]+")"
		count+=1
	menu()


def main():
	scan()
	menu()



if __name__ == "__main__":
    main()

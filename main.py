from wifi import Cell, Scheme
import os

interfaz = 'wlxc04a00118487'
#interfaz = raw_input('Network interface: ')
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
for red in redes:
	print "- ", red[0],"(ID = ",count,")"
	print "   Info: ("+red[1]+", "+red[2]+", "+red[3]+", "+red[4]+", "+red[5]+")"
	count+=1

id_red = raw_input('Select id: ')
password = raw_input('Password: ')
#cell = list_[int(id_red)]
#scheme = Scheme.for_cell(interfaz, 'home', cell, password)
#scheme.delete()
#scheme.save()
#scheme.activate()

essid=redes[int(id_red)][0]
conf_file="supp.conf"
#command = "echo 'ctrl_interface=/var/run/wpa_supplicant \nnetwork={\n   ssid=\""+essid+"\"\n   scan_ssid=1\n   proto=WPA\n   key_mgmt=WPA-PSK\n   psk=\""+password+"\"\n}' > "+conf_file
#os.system(command)

os.system( "(wpa_passphrase W4nd4Wifi wandafortea1212) >> " + conf_file)

#os.system("wpa_supplicant -B -w -c "+conf_file+" -D wext -i "+interfaz)
os.system("wpa_supplicant -Dnl80211 -i "+interfaz+" -c "+conf_file)

#os.system("rm "+conf_file)


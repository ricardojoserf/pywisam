from wifi import Cell, Scheme
import os

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
for red in redes:
	print "- ", red[0],"(ID = ",count,")"
	print "   Info: ("+red[1]+", "+red[2]+", "+red[3]+", "+red[4]+", "+red[5]+")"
	count+=1

id_red = raw_input('Select id: ')
password = raw_input('Password: ')

essid=redes[int(id_red)][0]
conf_file="supp.conf"

os.system( "wpa_passphrase "+essid+" "+password+" > " + conf_file)
os.system("wpa_supplicant -Dnl80211 -i "+interfaz+" -c "+conf_file+" &")
#os.system("rm "+conf_file)


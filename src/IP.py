
class IP:
    __IP = 0
    __ID = 0
    __Broadcast = 0
    __Mask = 0
    __Cidr = 0
    
    @staticmethod
    def str_dec(ipStr):
        temp = ipStr.split(".")
        result = 0
        if (len(temp) != 4):
            return False
        for i in range(0, 4):
            result = result + (int(temp[i]) << (8 *(3-i)) )
        return result
        
    @staticmethod
    def dec_str(dec):
        #return str((dec >> 24) & 255) + "." + str((dec & 0xff0000) >>16) + "." + str((dec & 0xff00) >>8) + "." + str(dec & 0xff)  
        return "%d.%d.%d.%d" %( (dec >> 24) & 255 , (dec >> 16) & 255 , (dec >> 8)  & 255 , dec & 255);
        

    def __init__(self, ip, cidr = 0):
        '''
            Save Everything in Decimal or Int form, so that we can calculate
        '''
        self.__IP = IP.str_dec(ip)
        self.__Cidr = cidr
        self.__Mask = (~0 << (32 - cidr));
        self.generate()
    def generate(self):
        self.__ID = self.__IP & self.__Mask
        self.__Broadcast = self.__ID | ~self.__Mask

    
    def setPrefix(self, prefix):
        # /0 = 0.0.0.0 to /32 = 255.255.255.255
        # but only /8 to /30 is a valid
        # because /8 has 16777216 and /30 has 2 host
        self.__Cidr = prefix
        '''
        if ( 0 <= prefix <= 32):
            mask = '.'.join([str((0xffffffff << (32 - prefix) >> i) & 0xff) for i in [24, 16, 8, 0]])
            print mask
            self.__Mask = IP.str_dec(mask)
        else:
            print "bad"
        '''
        self.__Mask = (~0 << (32 - prefix));

    ### ---------- [ Getter ] ---------- ###
    def getIP(self): return IP.dec_str(self.__IP)
    def getMask(self): return IP.dec_str(self.__Mask)
    def getCidr(self): return self.__Cidr
    def getID(self): return IP.dec_str(self.__ID)       
    def getBroadcast(self): return IP.dec_str(self.__Broadcast)
    def getHostCount(self): 
        # 2^(32 - Cidr) -2
        # Assuming Cidr = 24
        # 2^(32 - 24) -2 = 254 
        # So /24 network can assign 254 hosts.
        return self.__Broadcast - self.__ID - 1
    def getFirst(self): return IP.dec_str(self.__ID + 1)
    def getLast(self): return IP.dec_str(self.__Broadcast - 1)

    def getWildcast(self): return IP.dec_str(4294967295 - self.__Mask)

    ### ---------- [ Function ] ---------- ###
    def contains(self, ip):
        if self.__ID < ip and ip < self.__Broadcast: return True
        else: return False
    def isLinkLocal(self):
        # 169.254.0.0/16 or APIPA in MsWindows
        return IP("169.254.0.0", 16).contains(self.__IP)
    def isLoopback(self):
        # 127.0.0.0/8
        # if 2130706432 < self.__IP < 2147483647: return True
        return IP("127.0.0.0", 8).contains(self.__IP)
    def isPrivate(self):
        # 10.0.0.0/8 => 10.0.0.0-10.255.255.255
        # 172.16.0.0/12 => 172.16.0.0-172.31.255.255
        # 192.168.0.0/16 => 192.168.0.0-192.168.255.255
        return IP("10.0.0.0", 8).contains(self.__IP) or IP("172.16.0.0", 12).contains(self.__IP) or IP("192.168.0.0", 16).contains(self.__IP)

    def getClass(self):
        # Class A from   0.0.0.0 to 127.255.255.255
        # Class B from 128.0.0.0 to 191.255.255.255
        # Class C from 192.0.0.0 to 223.255.255.255
        # Class D from 224.0.0.0 to 239.255.255.255 // Multicast
        # Class E from 240.0.0.0 to 255.255.255.255 // Reversed
        pass
    def getVersion(self):
        return 4
    
    def info(self):
        print " --- [%s/%s] --- "%(self.getIP(), self.__Cidr)
        print " Network ID        : ", self.getID()
        print " Broadcast Address : ", self.getBroadcast()
        print " Subnet Mask       : ", self.getMask()
        print " Wildcast Mask     : ", self.getWildcast()
        print " Total host count  :  %d from %s to %s" %(self.getHostCount(), self.getFirst(), self.getLast())
    def display(self):
        ''' Aliance to info() '''
        self.info()

if __name__ == '__main__':
    ip = IP('192.168.1.190', 24)
    ip.display()

'''
>>> ip = IP('192.168.1.1', 24)
>>> ip.info()
=== [ 192.168.1.1/24 ] ===
Network ID        : 192.168.1.0
Broadcast Address : 192.168.1.255
Subnet Mask       : 255.255.255.0
Wildcast Mask     : 0.0.0.255
Total host count  : 254 from 192.168.1.1 to 192.168.1.254
>>> ip = IP('192.168.1.128', '255.255.255.128')
>>> ip.info()
=== [ 192.168.1.1/25 ] ===
Network ID        : 192.168.1.128
Broadcast Address : 192.168.1.255
Subnet Mask       : 255.255.255.128
Wildcast Mask     : 0.0.0.128
Total host count  : 126 from 192.168.1.1 to 192.168.1.254
>>> ipList = ip.all() # return List of usable Host IP
>>> len(ipList)
126
>>> ip = IP('127.0.0.1')  # without second argument default to 255.255.255.255(/32) 1 only host
>>> ip.isLoopback()
True
>>> ip = IP('169.1.1.1')
>>> ip.isLinkLocal()
True
>>> ip = IP('172.16.0.1')
>>> ip.isPrivate()
True
# toBin(), toOct(), toDec(), toHex(), toStr()
# isValid()
# fromBin(), fromOct(), fromDec(),
# getID(), getCidr(), getBroadcast(), getWildcast()
# getFirst(), getLast(), getHostCount()
'''
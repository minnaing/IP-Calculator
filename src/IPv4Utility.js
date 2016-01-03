
/**
Name: IPv4Utility
Version: 0.1.0
Author: Han M. Naing

*/


// http://www.w3resource.com/javascript/form/ip-address-validation.php
function ValidateIPaddress(ipStr){  
	var ipformat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;  
	if( ipStr.match(ipformat) ){  
		return true;  
 	} else {  
 		return false;  
 	}  
}
// --- END of Validation ---

var IPv4Utility = function(ipStr, cidr){
	this.ip = str_int(ipStr);
	this.cidr = cidr;
	this.mask = (~0 << (32 - cidr));
	this.network = this.ip & this.mask;
	this.broadcast = this.network | ~this.mask;
	console.log("int(IP) = " + this.ip);
	console.log("Net/Broad" + this.network + " --- " + this.broadcast);
	this.wildcast = int_str(~this.mask);// int_str(4294967295 - this.mask + 1);

	function int_str(int) {
	    var part1 = int & 255;
	    var part2 = ((int >> 8) & 255);
	    var part3 = ((int >> 16) & 255);
	    var part4 = ((int >> 24) & 255);

	    return part4 + "." + part3 + "." + part2 + "." + part1;
	}
	function str_int(str){
		var d = str.split('.');
    	return ((((((+d[0])*256)+(+d[1]))*256)+(+d[2]))*256)+(+d[3]);
	};
	
	this.get_network = int_str(this.network);
	this.get_subnet = int_str(this.mask);
	
	this.get_first = int_str(this.network +1);
	this.get_last = int_str(this.broadcast -1);
	this.get_broadcast = int_str(this.broadcast);
	this.count = this.broadcast - this.network - 1;
	this.contains = function(){};

	// More Option

	// Class A from   0.0.0.0 to 127.255.255.255 => 
    // Class B from 128.0.0.0 to 191.255.255.255
    // Class C from 192.0.0.0 to 223.255.255.255
    // Class D from 224.0.0.0 to 239.255.255.255 // Multicast
    // Class E from 240.0.0.0 to 255.255.255.255 // Reversed

    function get_the_class(ip){
    	if (0 <= ip && ip <= 2147483647) { return 'Class A'; }
    	else if (2147483648 <= ip && ip <= 3221225471) { return 'Class B'; }
    	else if (3221225472 <= ip && ip <= 3758096383) { return 'Class C'; }
    	else if (3758096384 <= ip && ip <= 4026531839) { return 'Class D'; }
    	else if (4026531840 <= ip && ip <= 4294967295) { return 'Class E'; }	
    	else { return ''; }
    };
    this.get_class = get_the_class(this.ip);
    console.log(this.get_class);

    // Loopback Address
	// 127.0.0.0/8 => 2130706432 - 2147483647
	this.isLoopback = 2130706432 <= this.ip && this.ip <= 2147483647;
	
	// Link Local or APIPA in MsWindows
	// 169.254.0.0/16 => 169.254.192.0 - 169.254.255.255 => 2851995648 - 2852061183
	this.isLinkLocal = 2851995648 <= this.ip && this.ip <= 2852061183;
	
	// Private Address
	// 10.0.0.0/8 => 10.0.0.0-10.255.255.255 => 167772160 - 184549375
    // 172.16.0.0/12 => 172.16.0.0-172.31.255.255 => 2886729728 - 2887778303
    // 192.168.0.0/16 => 192.168.0.0-192.168.255.255 => 3232235520 - 3232301055
    this.isPrivate =   (167772160 <= this.ip && this.ip <= 184549375)
    				|| (2886729728 <= this.ip && this.ip <= 2887778303)
    				|| (3232235520 <= this.ip && this.ip <= 3232301055);

};
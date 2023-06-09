# Coen-HW-3

Shubham Kamdi 
COEN 243 HW - 3
Mininet and OpenFlow
1609266

Task 1 - Defining custom topologies

1. What is the output of “nodes” and “net”? 
\
Nodes => Gives the all the individual nodes in the current topology 
\
c0 h1 h2 h3 h4 h5 h6 h7 h8 s1 s2 s3 s4 s5 s6 s7
\
Net => It will display all links of the current topology
\
```
h1 h1-eth0:s3-eth2
h2 h2-eth0:s3-eth3
h3 h3-eth0:s4-eth2
h4 h4-eth0:s4-eth3
h5 h5-eth0:s6-eth2
h6 h6-eth0:s6-eth3
h7 h7-eth0:s7-eth2
h8 h8-eth0:s7-eth3
s1 lo:  s1-eth1:s2-eth1 s1-eth2:s5-eth1
s2 lo:  s2-eth1:s1-eth1 s2-eth2:s3-eth1 s2-eth3:s4-eth1
s3 lo:  s3-eth1:s2-eth2 s3-eth2:h1-eth0 s3-eth3:h2-eth0
s4 lo:  s4-eth1:s2-eth3 s4-eth2:h3-eth0 s4-eth3:h4-eth0
s5 lo:  s5-eth1:s1-eth2 s5-eth2:s6-eth1 s5-eth3:s7-eth1
s6 lo:  s6-eth1:s5-eth2 s6-eth2:h5-eth0 s6-eth3:h6-eth0
s7 lo:  s7-eth1:s5-eth3 s7-eth2:h7-eth0 s7-eth3:h8-eth0
c0
```
2. What is the output of “h7 ifconfig”
\
"h7 ifconfig" would display the network configuration which includes IP address, broadcast address and MAC address of the host h7.
```
h7-eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.0.7  netmask 255.0.0.0  broadcast 10.255.255.255
        inet6 fe80::40db:47ff:fe97:e981  prefixlen 64  scopeid 0x20<link>
        ether 42:db:47:97:e9:81  txqueuelen 1000  (Ethernet)
        RX packets 56  bytes 4232 (4.2 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10  bytes 796 (796.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        
        lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Task 2 - Analyze the “of_tutorial’ controller
\
1. Draw the function call graph of this controller. For example, once a packet comes to the
controller, which function is the first to be called, which one is the second, and so forth?

```
	packet comes in
	
        |
        V
	,__________________,
	|                  |
	| _handle_PacketIn |
	|__________________|
	
	    |
	    V
	,__________________,
	|                  |
	|   act_like_hub   |   
	|__________________|
	
	    |
	    V
	,__________________,
	|                  |
	|  resend_packet   |
	|__________________|
		
	    |
	    V

     forward message to port
```
\
2. Have h1 ping h2, and h1 ping h8 for 100 times (e.g., h1 ping -c100 p2).
\
2a. How long does it take (on average) to ping for each case?
```
h1 ping h2 : 7.052 ms
h1 ping h8 : 28.928 ms 
```
2b.  What is the minimum and maximum ping you have observed?
```
h1 ping h2:
min =>  0.787
max => 194.158

h1 ping h8:
min => 9.068 
max => 311.135
```
\
2c. What is the difference, and why?
```
It has been noticed that the time taken for a ping packet to travel from host h1 to h8 is considerably longer than the time taken for a ping packet to travel from h1 to h2. This difference in ping times could be attributed to the fact that the packet must traverse through multiple switches from h1 to h8, whereas only one switch is involved in the path between h1 and h2.
```
\
3. Run “iperf h1 h2” and “iperf h1 h8”
\
3a. What is “iperf” used for?
```
"Iperf" is a commonly used tool for measuring network bandwidth and performance. It is used to test the maximum achievable bandwidth between two network endpoints by generating and transmitting a stream of data packets, and then measuring the rate at which the packets are received at the other end.
```
\
3b. What is the throughput for each case?
```
h2 h2:
Server - 9.00 Mbits/sec 
Client - 9.55 Mbits/sec 

h1 h8:
Server - 3.00 Mbits/sec 
Client - 4.00 Mbits/sec 
```

3c. What is the difference, and explain the reasons for the difference. 
```
The observed data transfer rate between h1 and h8 is less than half of the data transfer rate between h1 and h2. This is because when a packet is transmitted through multiple switches, each switch has to broadcast the incoming packet to every other node, which takes more time.However, since h1 and h2 are connected by only one switch, the transfer rate is faster as there are no other switches involved in the transmission.
```
4. Which of the switches observe traffic? 
```
All switches observe traffic.
```

Task 3 - MAC Learning Controller
\
1. Describe how the above code works, such as how the "MAC to Port" map is established. You could use a ‘ping’ example to describe the establishment process (e.g., h1 ping h2). 
```
When h1 sends a ping packet to h2, the packet is routed through switch 's3'. While routing, switch 's3' searches the mac_to_port{} table to check if it already contains a record for the MAC address of the incoming packet. If an entry is found, the switch forwards the packet to the port that matches the MAC address. If there is no matching entry, the switch learns the association between the MAC address and the input port of the packet, adds the entry to the mac_to_port{} table, and then broadcasts the packet to all output ports except the input port.
```
2. Have h1 ping h2, and h1 ping h8 for 100 times (e.g., h1 ping -c100 p2). 
\
2a. How long did it take (on average) to ping for each case?
```
h1 ping h2 : 13.000  ms
h1 ping h8 : 33.000 ms
```
2b. What is the minimum and maximum ping you have observed? 
```
h1 ping h2:
Min => 1.210 ms
Max => 103.000 ms

h1 ping h8:
Min => 14.062 ms
Max => 225.0 ms
```
2c. Any difference from Task 2 and why do you think there is a change if there is?
```
Despite the fact that the average ping time is a bit higher than in Task2, the minimum and maximum ping values are considerably lower.This is due to the switch being more knowledgeable about the network by storing the known MAC addresses, which reduces the need to broadcast incoming packets to every other switch. Consequently, the switch only needs to transfer packets to a single known address, thereby reducing the overall transmission time and resulting in a lower ping time.
```
3. Run “iperf h1 h2” and “iperf h1 h8”.
\
3a. What is the throughput for each case?
```
h2 h2:
Server - 645 Kbits/sec
Client - 890 Kbits/sec

h1 h8:
Server - 170 Kbits/sec
Client - 360 Kbits/sec
```

3b. What is the difference from Task 2 and why do you think there is a change if there is?
```
Not sure why but there is a huge difference in throughput. 
```

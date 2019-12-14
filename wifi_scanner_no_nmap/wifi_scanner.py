#!/anaconda3/bin/python
import socket
import re
import subprocess, os
import platform
from ipaddress import ip_network, IPv4Network, IPv4Address, ip_address
import time
from threading import Lock, Thread
from getmac import get_mac_address


def scan_network(target_net: IPv4Network):

    active_hosts = []   # all active host ip 
    lock = Lock()   # for threading
    threads = []    # all threads

    # to direct output of subprocess to
    FNULL = open(os.devnull, 'w')

    def ping(ip):
        # windows ping uses -n instead of -c
        param = '-n' if platform.system().lower()=='windows' else '-c'

        command = ['ping', param, '1', ip]

        # call ping command
        result = subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT)
       
        # if ping successful
        if result == 0:
            lock.acquire()
            active_hosts.append(ip)
            lock.release()

    start_time = time.time()
    print(f"Scanning {target_net.compressed}...", end="\n\n")

    # iterate through hosts
    for host in target_net.hosts():
        host_ip = str(host.compressed)
        t = Thread(target=ping, args=(host_ip, ))
        threads.append(t)
        threads[-1].start()
    
    for thread in threads:
        thread.join()

    # display hosts and information
    print(f"Found {len(active_hosts)} active hosts.")

    for count, host_ip in enumerate(active_hosts):
        print(f"\nHost {count + 1}")
        print("-----------------------")
        try:
            hostname = socket.gethostbyaddr(host_ip)[0]
        except socket.herror:
            hostname = "Unknown"
        host_mac = get_mac_address(ip=host_ip)

        print(f"Host:\t{hostname}")
        print(f"IP:\t{host_ip}")
        print(f"MAC:\t{host_mac}")

        time.sleep(.5)
        

    # elapsed_time = (dt.datetime.now() - start_time).total_seconds()
    elapsed_time = time.time() - start_time
    print(f"\nNetwork Scan Finished.\nTime Elapsed: {elapsed_time:.3f} seconds.")

    os._exit(1)

# main process
def main():
    print('''
      _____         .__            /\          __      __._____________.__    _________                                          
  /  _  \   _____|__| ____   ___)/  ______ /  \    /  \__\_   _____/|__|  /   _____/ ____ _____    ____   ____   ___________  
 /  /_\  \ /  ___/  |/ __ \ /    \ /  ___/ \   \/\/   /  ||    __)  |  |  \_____  \_/ ___\\__  \  /    \ /    \_/ __ \_  __ \ 
/    |    \\___ \|  \  ___/|   |  \\___ \   \        /|  ||     \   |  |  /        \  \___ / __ \|   |  \   |  \  ___/|  | \/ 
\____|__  /____  >__|\___  >___|  /____  >   \__/\  / |__|\___  /   |__| /_______  /\___  >____  /___|  /___|  /\___  >__|    
        \/     \/        \/     \/     \/         \/          \/                 \/     \/     \/     \/     \/     \/        
    ''')
    # check if input is ipv4 with cidr notation
    while True:
        target_net = input("Please enter target network to scan: ")

        if re.match('(\d+[.]){3}\d+/\d+', target_net):
            target_net: IPv4Network = ip_network(target_net)
            break
        elif re.match('(\d+[.]){3}\d+', target_net):
            print("Please enter a network not a single host.")
        else:
            print("Please enter valid IPv4 address with CIDR notation.")

    scan_network(target_net)

        
if __name__ == "__main__":
    main()
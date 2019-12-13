# pip3 install python-nmap
# pip3 install getmac
import nmap
import time
import datetime as dt
from getmac import get_mac_address

def scan_network(target_net):
    # start_time = dt.datetime.now()
    start_time = time.time()
    print(f"Scanning {target_net}...", end="\n\n")

    nm = nmap.PortScanner()
    nm.scan(hosts=target_net, arguments="-sP")

    print(f"Found {len(nm.all_hosts())} active hosts.", end="\n")

    for count, host in enumerate(nm.all_hosts()):
        print(f"\nHost {count + 1}")
        print("----------------------")
        if nm[host].hostname() != "":
            print(f"Host:\t{nm[host].hostname()}")
        else:
            print("Host:\tUnknown")
        print(f"IP:\t{host}")
        print(f"MAC:\t{get_mac_address(ip=host)}")

        time.sleep(.5)

    # elapsed_time = (dt.datetime.now() - start_time).total_seconds()
    elapsed_time = time.time() - start_time
    print(f"\nNetwork Scan Finished.\nTime Elapsed: {elapsed_time:.3f} seconds.")

def main():
    print('''
      _____         .__            /\          __      __._____________.__    _________                                          
  /  _  \   _____|__| ____   ___)/  ______ /  \    /  \__\_   _____/|__|  /   _____/ ____ _____    ____   ____   ___________  
 /  /_\  \ /  ___/  |/ __ \ /    \ /  ___/ \   \/\/   /  ||    __)  |  |  \_____  \_/ ___\\__  \  /    \ /    \_/ __ \_  __ \ 
/    |    \\___ \|  \  ___/|   |  \\___ \   \        /|  ||     \   |  |  /        \  \___ / __ \|   |  \   |  \  ___/|  | \/ 
\____|__  /____  >__|\___  >___|  /____  >   \__/\  / |__|\___  /   |__| /_______  /\___  >____  /___|  /___|  /\___  >__|    
        \/     \/        \/     \/     \/         \/          \/                 \/     \/     \/     \/     \/     \/        
    ''')
    target_net = input("Please enter target network to scan: ")

    scan_network(target_net)
    

if __name__ == "__main__":
    main()
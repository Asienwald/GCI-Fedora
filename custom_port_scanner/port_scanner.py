import socket
import os
from threading import Thread, Lock
import re
import time

# common ports to use
COMMON_PORTS = (20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 135, 139, 143, 
                443, 445, 3389)

lock = Lock()
threads = []

open_ports = []



def scan_port(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        conn = s.connect_ex((target_ip, port))

        if conn == 0:
            lock.acquire()
            open_ports.append(port)
            lock.release()
    except OSError:
        pass

def scan_ports(target_ip, scan_common: bool, scan_start, scan_end):
    start_time = time.time()

    print(f"Scanning host at {target_ip}...", end="\n\n")
    
    if scan_common:
        print("Scanning for common ports...")
        for port in COMMON_PORTS:
            t = Thread(target=scan_port, args=(target_ip, port))
            threads.append(t)
            threads[-1].start()
            
        print("\n")
    else:
        print(f"Scanning ports {scan_start} to {scan_end}...")
        for port in range(scan_start, scan_end):
            t = Thread(target=scan_port, args=(target_ip, port))
            threads.append(t)
            threads[-1].start()
            

    for thread in threads:
        thread.join()

    for port in open_ports:
        print(f"Port {port} is open.")

    elapsed_time = time.time() - start_time
    print(f"\nPort scan finished.\nTime elapsed: {elapsed_time:.3f} seconds.")
    
    os._exit(1)


def main():
    print('''
  ,---.         ,--.               ,--.          ,------.                 ,--.       ,---.                                               
 /  O  \  ,---. `--' ,---. ,--,--, |  |,---.     |  .--. ' ,---. ,--.--.,-'  '-.    '   .-'  ,---. ,--,--.,--,--, ,--,--,  ,---. ,--.--. 
|  .-.  |(  .-' ,--.| .-. :|      \`-'(  .-'     |  '--' || .-. ||  .--''-.  .-'    `.  `-. | .--'' ,-.  ||      \|      \| .-. :|  .--' 
|  | |  |.-'  `)|  |\   --.|  ||  |   .-'  `)    |  | --' ' '-' '|  |     |  |      .-'    |\ `--.\ '-'  ||  ||  ||  ||  |\   --.|  |    
`--' `--'`----' `--' `----'`--''--'   `----'     `--'      `---' `--'     `--'      `-----'  `---' `--`--'`--''--'`--''--' `----'`--'    
                                                                                                             
''')
    # Input validations with regex
    while True:
        target_ip = input("Enter IP to scan: ")
        if re.match('(\d+[.]){3}\d+', target_ip):
            break
        else:
            print("Please enter valid IP.", end="\n\n")
    while True:
        scan_common = input("Do you want to scan for common ports only? (y/n): ")
        if re.match('[yY]', scan_common):
            scan_common = True
            scan_start, scan_end = 0, 0
            break
        elif re.match('[nN]', scan_common):
            scan_common= False
            while True:
                scan_range = input("Input port range to scan (1-65535): ")
                if re.match('\d+-\d+', scan_range):
                    scan_range = scan_range.split("-")
                    scan_start, scan_end = int(scan_range[0]), int(scan_range[1])
                    if scan_start > scan_end:
                        print("Input valid range.", end="\n\n")
                        continue
                    else:
                        break
                else:
                    print("Please enter valid range of x-y.", end="\n\n")
            break
        else:
            print("Please input a valid response.", end="\n\n")
    
    # begin port scans
    scan_ports(target_ip, scan_common, scan_start, scan_end)

if __name__ == '__main__':
    main()
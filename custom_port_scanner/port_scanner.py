import socket
import os
import threading
import re
import time
import datetime as dt

# common ports to use
COMMON_PORTS = (20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 135, 139, 143, 
                443, 445, 3389)

def scan_port(target_ip, port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    conn = s.connect_ex((target_ip, port))

    if conn == 0:
        print(f"Port {port} is open.", end="\n")
        time.sleep(1)
    # else:
    #     print("nope")

def scan_ports(target_ip, scan_common: bool, scan_start, scan_end):
    # start_time = time.process_time()
    start_time = dt.datetime.now()

    print(f"Scanning host at {target_ip}...", end="\n\n")
    
    
    if scan_common:
        print("Scanning for common ports...")
        for port in COMMON_PORTS:
            t = threading.Thread(target=scan_port, args=(target_ip, port))
            t.start()
            time.sleep(.1)
        print("\n")

    print(f"Scanning ports {scan_start} to {scan_end}...")
    for port in range(scan_start, scan_end):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        t.start()
        time.sleep(.01)  

    # elapsed time calculation doesn't work when using multithreading
    elapsed_time = (dt.datetime.now() - start_time).total_seconds()
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
        scan_common = input("Do you want to scan for common ports? (y/n): ")
        if re.match('[yY]', scan_common):
            scan_common = True
            break
        elif re.match('[nN]', scan_common):
            scan_common= False
            break
        else:
            print("Please input a valid response.", end="\n\n")
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
    # begin port scans
    scan_ports(target_ip, scan_common, scan_start, scan_end)

if __name__ == '__main__':
    main()
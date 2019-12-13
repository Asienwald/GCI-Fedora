import hashlib as hl
import sys
import os
import time
import urllib.request as urllib
# pip3 install pyperclip
import pyperclip

# show all algo available
# print(hl.algorithms_available)

# hash types available
HASH_TYPES = ("MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512")
# hash bytes mapping
HASH_BYTES = {128: 1, 160: 2, 224: 3, 256: 4, 384: 5, 512: 6}

# determine hash function to use with index given
def determine_hash_type(hash_type: int):
    if hash_type == 1: # MD5
        hash_func = hl.md5
    elif hash_type == 2: # SHA1
        hash_func = hl.sha1
    elif hash_type == 3: # SHA224
        hash_func = hl.sha224
    elif hash_type == 4: # SHA256
        hash_func = hl.sha256
    elif hash_type == 5: # SHA384
        hash_func = hl.sha384
    elif hash_type == 6: # SHA512
        hash_func = hl.sha512

    return hash_func

# hash provided string
def hash_string():
    # choose hash type based on its index
    while True:
        hash_type = input('''\nChoose Hash Type:
1. MD5
2. SHA1
3. SHA224
4. SHA256
5. SHA384
6. SHA512
>>> ''')
        if hash_type.isnumeric():
            hash_type = int(hash_type)
            if hash_type < 1 or hash_type > 6:
                print("Type chosen out of range.")
            else:
                break
        else:
            print("Invalid input. Must be numeric")
    print(f"{HASH_TYPES[hash_type - 1]} hash type chosen.\n")
    
    str_to_hash = input("Enter string to hash: ").encode("utf-8")

    # get function from hash type index
    hash_func = determine_hash_type(hash_type)

    # obtain hashed string
    hashed_str = hash_func(str_to_hash).hexdigest()
    
    print(f"Hashed result: {hashed_str}")

    # copy the hash to clipboard for convenience
    pyperclip.copy(hashed_str)
    print("Hash copied to clipboard!")

    print("Returning to menu...\n")
    hash_menu()


# crack hash with password list specified
def crack_hash_with_list(pwd_list_name, hash_func, uncracked_hash):

    # iterate through the password list given
    def iterate_list(encoding=False):
        for pwd in pwd_list:
            pwd = pwd.strip()
            
            # if lines in list are not bytes
            # rockyou.txt taken online is in the form of bytes hence don't need further encoding
            if encoding:
                hashed_pwd = hash_func(pwd.encode("utf-8")).hexdigest()
            else:
                hashed_pwd = hash_func(pwd).hexdigest()

            # check if hashes are equal
            if hashed_pwd == uncracked_hash:
                return pwd
        return ""

    try:
        # use online rockyou.txt password list if no list specified
        if pwd_list_name == "":
            with urllib.urlopen("https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt") as pwd_list:
                return iterate_list(encoding=False)
        else:
            file_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
            with open(file_dir + pwd_list_name, "r", encoding="utf-8") as pwd_list:
                return iterate_list(encoding=True)
    
    # specified file not found in directory
    except FileNotFoundError:
        print("Specified password list is not found in this directory.")
        print("Returning to menu...\n")
        hash_menu()

# funcion to crack hashes given
def crack_hash():
    start_time = time.time()

    # get hash to crack
    uncracked_hash = input("Enter hash to crack: ")

    # calculate bytesize of hash
    hash_bytesize = len(uncracked_hash) * 4

    # get hash type from bytesize
    try:
        hash_type = HASH_BYTES[hash_bytesize]
    except KeyError:
        print("Hash type can't be detected. Is the hash provided correct?")
        hash_menu()

    print(f"{HASH_TYPES[hash_type - 1]} hash type detected.\n")

    # determine hash function to use from hash type
    hash_func = determine_hash_type(hash_type)

    # get password list
    pwd_list_name = input("Enter password list to use (leave blank to use default rockyou.txt): ")
    print("Cracking now...\n")

    # try to crack hash with password list (return "" if can't crack)
    cracked_hash = crack_hash_with_list(pwd_list_name, hash_func, uncracked_hash)

    if cracked_hash == "":
        print("Provided hashed cannot be cracked. Try another one.")
    else:
        print(f"Hash cracked!\nTime Elapsed: {(time.time() - start_time):.3f} seconds.\n")
        if isinstance(cracked_hash, bytes):
            cracked_hash: bytes = cracked_hash.decode("utf-8")
        print(f"{uncracked_hash} -> {cracked_hash}")

    print("\nReturning to menu...\n")
    hash_menu()
    
# hash main menu
def hash_menu():
    while True:
        action = input('''Specify action to take:
1. Hash a string
2. Crack a hash (no salting)
3. Exit
>>> ''')
        if action.isnumeric():
            action = int(action)
            if action not in [1, 2, 3]:
                print("Invalid action.\n")
            else:
                break
        else:
            print("Please input a number.\n")

    if action == 1:
        hash_string()
    elif action == 2:
        crack_hash()
    elif action == 3:
        print("Exiting...")
        sys.exit(1)


def main():
    print('''
       _____         .__            /\           ___ ___               .__                   
  /  _  \   _____|__| ____   ___)/  ______  /   |   \_____    _____|  |__   ___________  
 /  /_\  \ /  ___/  |/ __ \ /    \ /  ___/ /    ~    \__  \  /  ___/  |  \_/ __ \_  __ \ 
/    |    \\___ \|  \  ___/|   |  \\___ \  \    Y    // __ \_\___ \|   Y  \  ___/|  | \/ 
\____|__  /____  >__|\___  >___|  /____  >  \___|_  /(____  /____  >___|  /\___  >__|    
        \/     \/        \/     \/     \/         \/      \/     \/     \/     \/        
    ''')

    hash_menu()


if __name__ == "__main__":
    main()
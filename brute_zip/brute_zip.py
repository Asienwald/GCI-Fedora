from zipfile import ZipFile, BadZipFile
import urllib.request as urllib
import os
import time

file_dir = os.path.dirname(os.path.realpath(__file__)) + "/"

def brute_zip(zip_name, pwd_list_name):

    def try_pwd(pwd):
        pwd = pwd.encode('utf-8')
        try:
            zf.extractall(file_dir, pwd=pwd)
            # password works!
            return pwd
        except RuntimeError:
            # password wrong (bad password)
            return ""
        except BadZipFile:
            return ""

    def iterate_pwd(encoding=True):
        for pwd in pwd_list:
            pwd = pwd.strip()
            
            # if lines in list are not bytes
            # rockyou.txt taken online is in the form of bytes hence don't need further encoding
            if not encoding:
                try:
                    pwd = pwd.decode('utf-8')
                except UnicodeDecodeError:
                    pass
            result = try_pwd(pwd)

            # pwd don't work
            if result == "":
                continue
            else:
                return pwd
        # none of the passwords worked
        return pwd
    
    try:
        print("Bruting ZIP file...\n")

        with ZipFile(file_dir + zip_name) as zf:
            # use online rockyou.txt password list if no list specified
            if pwd_list_name == "":
                with urllib.urlopen("https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt") as pwd_list:
                    return iterate_pwd(encoding=False)
            else:
                with open(file_dir + pwd_list_name, "r") as pwd_list:
                    return iterate_pwd()
    
    # specified file not found in directory
    except FileNotFoundError:
        print("Either the zip file or password file cannot be found.")
        print("Please try again.") 
    except urllib.URLError:
        print("You need internet connection to use the default rockyou.txt password list.")


def main():
    print('''
                                     )             
   (                 )        ( /(             
 ( )\  (      (   ( /(   (    )\()) (          
 )((_) )(    ))\  )\()) ))\  ((_)\  )\  `  )   
((_)_ (()\  /((_)(_))/ /((_)  _((_)((_) /(/(   
 | _ ) ((_)(_))( | |_ (_))   |_  /  (_)((_)_\  
 | _ \| '_|| || ||  _|/ -_)   / /   | || '_ \) 
 |___/|_|   \_,_| \__|\___|  /___|  |_|| .__/  
                                       |_|     
    ''')
    zip_name = input("Enter ZIP file to brute: ")
    pwd_list_name = input("Enter password list to use (leave blank to use default rockyou.txt): ")

    start_time = time.time()
    result = brute_zip(zip_name, pwd_list_name)

    if result == "":
        print("Password of ZIP file could not be found.")
    else:
        elapsed_time = time.time() - start_time
        print("Brute Successful!\n")
        print(f"Password of ZIP file is <{result}>.")
        print("Contents of ZIP file extracted to current file directory.\n")
        print(f"Elapsed time: {elapsed_time:.3f} seconds.")
    
    print("Exitting...")


if __name__ == '__main__':
    main()
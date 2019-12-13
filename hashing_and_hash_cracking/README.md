# Asien Hasher
Simple hashing and cracking script built with Python
![](https://i.imgur.com/xjnJc8C.png)

## Usage
### Run the Script
In your terminal, run `python hasher.py`


### Pick Action - Hash
Pick hashing algorithm to use.

![](https://i.imgur.com/Tx8FNwU.png)

Input desired string to hash.

Once completed, computed hash will be displayed and copied to your clipboard for convenience

![](https://i.imgur.com/qGME3ZA.png)


### Pick Action - Crack
Choose the crack hash option and input your hash

__Note: Hashes with salting is not supported!__

From the entered hash, it's type will be detected.

![](https://i.imgur.com/NtVq0GX.png)

Enter the name of your password list or leave it blank to use the default rockyou.txt

> Rockyou.txt is retrieved online.
> [Link here](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)

Else, you can specify your own password list.
Password list location is relative to the `hasher.py` script.

Script will then start cracking your hash and it will be displayed if successful

![](https://i.imgur.com/AjJiKKz.png)




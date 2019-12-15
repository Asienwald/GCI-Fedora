# Reverse Binary Files
GCI Task to reverse a set of binary files.
[Link Here](https://github.com/nishantparhi/Crackit-GCI)

## Overview
- From the headers of all 3 files, they are using the ELF file format, version 1
![](https://i.imgur.com/PHoq74K.png)
- All files coded in C

## Reversing the Files
- Used Radare2 for binary analyser

### 1st File
This file is rather easy. Just load it into a hex editor and the password can be seen in plaintext.

![](https://i.imgur.com/Gya3rIU.png)

The next 2 passwords can be found in the binary analyzer.

![](https://i.imgur.com/fjeb1ru.png)

Even though they look like bytes, they're actually strings.

__1st Password: FEDORAGCIPASSEASY__
__2nd Password: 0x1337__
__3rd Password: 0x133337__

### 2nd File
This binary file required us to use a binary analyzer tool, in this case Radare2

- Firstly, we load the bin file into Radare using `r2 2ndcrackme`

- Use the seek command to jump to the main function of the program
    - `s main`
- type `v` to enter visual mode

![](https://i.imgur.com/NRnlcyd.png)

- From image above, we can tell the password used for the binary file

__Password: FEd0raGCIt@sk__


### 3rd File
- basic information

![](https://i.imgur.com/3xR6CI2.png)

- find all strings in the file
    - pwd doesn't work. This is a troll (lol)

![](https://i.imgur.com/VpoPF6j.png)

- moving to main and analyzing the code there helped us find the password

![](https://i.imgur.com/QxLePtF.png)

__Password: 00g61@k00land1514cel!__



## Resources
- [Video explaining reversing ELF files](https://youtu.be/OBDuoqyZ4UA)
- [More on ELF](https://linux-audit.com/elf-binaries-on-linux-understanding-and-analysis/)
- [Radare2 Usage](https://medium.com/@jacob16682/reverse-engineering-using-radare2-588775ea38d5)

